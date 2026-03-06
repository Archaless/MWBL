"""
intercept_Serial.py

Read from one serial port, log timestamped data, and forward raw bytes to another serial port.
Uses Data_Transfer_Scripts.log2File for consistent logging when available.

This script is resilient to disconnections and will attempt to reconnect with exponential backoff.
Run with:
python3 /home/pi/Scripts/intercept_Serial.py --in-port /dev/ttyUSB0 --out-port /dev/ttyUSB1 --baud 19200 --log /var/log/serial_forward.log
"""

import argparse
import sys
import time
import signal
import threading
import traceback
from datetime import datetime, timezone
import serial
from serial.serialutil import SerialException
import Data_Transfer_Scripts as dts

STOP_EVENT = threading.Event()


def write_log(log_path, line):
    print(line)
    try:
        if dts is not None:
            dts.log2File(line, log_path)
        else:
            # Fallback to simple append
            with open(log_path, 'a') as f:
                f.write('\n' + str(datetime.now()) + ' - ' + line)
    except Exception:
        # Last resort: print to stderr
        print('LOGGING FAILED:', line, file=sys.stderr)

def forward_worker(src_ser, dst_ser, log_path, direction, hex_log, read_size):
    while not STOP_EVENT.is_set():
        try:
            data = src_ser.read(read_size)
            if not data:
                continue
            ts = datetime.now(timezone.utc).isoformat() + 'Z'
            if hex_log:
                dts.log2File(log_path, f'{ts} - {direction}: {data.hex()}')
            else:
                try:
                    text = data.decode('utf-8', errors='replace')
                except Exception:
                    text = repr(data)
                dts.log2File(log_path, f'{ts} - {direction}: {text}')
            try:
                dst_ser.write(data)
            except SerialException as e:
                dts.log2File(log_path, f'ERROR writing to {direction.split("->")[1]} serial: {e}')
                break
        except SerialException as e:
            dts.log2File(log_path, f'Serial read error ({direction}): {e}')
            break
        except Exception as e:
            dts.log2File(log_path, f'Unexpected error ({direction}): {e}')
            dts.log2File(log_path, traceback.format_exc())
            break

def forward_loop(in_port, out_port, log_path, hex_log=False, read_size=1024):
    backoff = 1
    while not STOP_EVENT.is_set():
        try:
            in_ser = None
            out_ser = None
            try:
                in_ser = serial.Serial(in_port['port'], in_port['baud'], in_port['timeout'], in_port['write_timeout'])
                out_ser = serial.Serial(out_port['port'], out_port['baud'], out_port['timeout'], out_port['write_timeout'])
            except SerialException as e:
                dts.log2File(log_path, f'SERIAL ERROR opening ports: {e}')
                time.sleep(backoff)
                backoff = min(backoff * 2, 60)
                continue

            backoff = 1
            dts.log2File(log_path, f'Opened serial ports IN={in_port["port"]} OUT={out_port["port"]}')

            # Start two threads for bidirectional forwarding
            t1 = threading.Thread(target=forward_worker, args=(in_ser, out_ser, log_path, "IN->OUT", hex_log, read_size))
            t2 = threading.Thread(target=forward_worker, args=(out_ser, in_ser, log_path, "OUT->IN", hex_log, read_size))
            t1.start()
            t2.start()
            # Wait for either thread to finish (error or STOP_EVENT)
            while t1.is_alive() and t2.is_alive():
                t1.join(timeout=0.5)
                t2.join(timeout=0.5)

            # Clean up
            try:
                in_ser.close()
            except Exception:
                pass
            try:
                out_ser.close()
            except Exception:
                pass

        except Exception as e:
            dts.log2File(log_path, f'Fatal loop error: {e}')
            dts.log2File(log_path, traceback.format_exc())
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)


def signal_handler(signum, frame):
    STOP_EVENT.set()


def parse_args(argv):
    p = argparse.ArgumentParser(description='Intercept serial data and forward it to another port')
    p.add_argument('--in-port', required=True, help='Input serial device (e.g. /dev/ttyUSB0)')
    p.add_argument('--out-port', required=True, help='Output serial device (e.g. /dev/ttyUSB1)')
    p.add_argument('--baud', type=int, default=9600, help='Baud rate for both ports')
    p.add_argument('--in-timeout', type=float, default=1.0, help='Read timeout (seconds)')
    p.add_argument('--out-timeout', type=float, default=1.0, help='Write timeout (seconds)')
    p.add_argument('--log', default='serial_forward.log', help='Path to log file')
    p.add_argument('--hex', action='store_true', help='Log raw data as hex string')
    p.add_argument('--read-size', type=int, default=1024, help='Bytes to read per iteration')
    return p.parse_args(argv)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    in_port = {'port': args.in_port, 'baud': args.baud, 'timeout': args.in_timeout, 'write_timeout': args.out_timeout}
    out_port = {'port': args.out_port, 'baud': args.baud, 'timeout': args.out_timeout, 'write_timeout': args.out_timeout}

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        forward_loop(in_port, out_port, args.log, hex_log=args.hex, read_size=args.read_size)
    except KeyboardInterrupt:
        STOP_EVENT.set()
    except Exception as e:
        write_log(args.log, f'Fatal error in main: {e}')
        write_log(args.log, traceback.format_exc())
        return 2

    return 0


if __name__ == '__main__':
    sys.exit(main())