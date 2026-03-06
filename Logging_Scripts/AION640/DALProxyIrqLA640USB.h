#ifndef __DALProxyIrqLA640USB_H__
#define __DALProxyIrqLA640USB_H__

#ifdef __cplusplus
extern "C" { /* using a C++ compiler */
#endif

#include <stdio.h>
#include <stdint.h>

#if (defined (LINUX) || defined (__linux__))
    typedef void *HANDLE;
#else
	#include <winsock2.h> // We don't want Windows.h to include winsock.h
	#include <Windows.h>
#endif

#ifdef __cplusplus
namespace DALProxyIrqLA640USB_namespace
{
#endif

#ifndef DOXYGEN
#if (defined (LINUX) || defined (__linux__))
    #ifdef DALProxyIrqLA640USB_LIBRARY
    #define DALProxyIrqLA640USB_API __attribute__((visibility("default")))
    #else
    #define DALProxyIrqLA640USB_API
    #endif
#else
    #ifdef DALProxyIrqLA640USB_LIBRARY
    #define DALProxyIrqLA640USB_API __declspec(dllexport)
    #else
    #define DALProxyIrqLA640USB_API __declspec(dllimport)
    #endif
#endif
#endif


/** \defgroup Module_Management Aion640 Management
  * \brief Establish and manage communication with Aion640.
  */

/** \defgroup Module_Processing Aion640 Processing
  * \brief Control Aion640 image processing.
  * Query module connected to workstation, Open and close link.
  */

/** \defgroup Module_Control Aion640 Control
  * \brief Set or Get module features. Refer to module user guide for details on features, and eDALProxyIrqLA640USBDeviceFeature for paeFeature definition.
  */

/** \defgroup Module_Image Aion640 Image
  * \brief Query Image from Aion640.
  */

/** \defgroup Module_Storage Aion640 Storage
  * \brief Store and retrieve processing settings into Aion640.
  */

/** \defgroup Module_Calibration Aion640 Calibration
  * \brief Manage calibration of Aion640.
  */

/** \defgroup Module_ErrFunc Function return codes
 * \brief Function execution returned codes.
  */

/** \defgroup Module_FeaturesTypes Features list
 * \brief Features list.
  */

/** \defgroup Module_AgcTypes Agc types
 * \brief Agc types list.
  */


/** \addtogroup Module_FeaturesTypes
  * \ref eDALProxyIrqLA640USBDeviceFeature enumerates all features to read/write.
  * \see Refer to module user guide for details on features
  *  @{ */

/** Enumeration list of features. */
DALProxyIrqLA640USB_API typedef enum
{
	eStrPartNumber = 0,
	eStrSerialNumber,
	eStrIRSensorSerialNumber,
	eStrFirmwareBuildDataTime,
	eiFirmware0Version,
	eiFirmware1Version,
	eiIsExportLimited,
	eiUSBSpeed,
	eiTimeStampClockFrequency,
	// IR Sensor Settings
	eiAnalogGain,
	efAnalogOffset,
	efAnalogOffsetMin,
	efAnalogOffsetMax,
    efRelativeAnalogOffset,
	eiIntegratorBWControl,
	eiAntiBloomingEnable,
	eiAntiBloomingValue,
	eiCDSFOPreventionEnable,
	eiCDSFOPreventionValue,
	eiCDSResetTime,
	eiColumnClampLevel,
	efVOS,
	efVOSMin,
	efVOSMax,
	efVDETCOM,
	efVDETCOMMin,
	efVDETCOMMax,
	eiHorizontalFlip,
	eiVerticalFlip,
	eiMasterBiasCurrent,
	eiCurrentLimitedLogicBias,
	eiIntegratorBias,
	eiColumnBufferBias,
	eiOutputDriverBias,
	eiOutputMultiplexerBias,
	efFPATemp,
	// Sequencer
	eiTriggerMode,
	efFrameRate,
	efFrameRateMin,
	efFactoryMaxFrameRate,
	efIntTime,
	efIntTimeMin,
	efIntTimeMax,
	eiIMROEnable,
	eiIMROCount,
	// Region of interest
	eiROI_H_size,
	eiROI_H_size_min,
	eiROI_H_size_max,
	eiROI_V_size,
	eiROI_V_size_min,
	eiROI_V_size_max,
	eiROI_X_pos,
	eiROI_X_pos_min,
	eiROI_X_pos_max,
	eiROI_Y_pos,
	eiROI_Y_pos_min,
	eiROI_Y_pos_max,
	// Video Stream
	eiVideoPattern,
	eiImageWidth,
	eiImageHeight,
	eiImagePixelFormat,
	eiUSBPayloadSize,
	eiVideoUSBOutputActivation,
	eiVideoDF12OutputActivation,
	// Configuration
	eiSave,
	eiRestore,
	eiLastConfig,
	// Table NUC
	eiLastSavedGainTable,
	eiLastSavedOffsetTable,
	// Darkness current
	eiLastSavedDarknessTable,
	// Built in self test
	eiBISTAction,
	eiBISTStatus,
	// Last
	eDeviceFeatureTotal
} eDALProxyIrqLA640USBDeviceFeature;

//! @}

/** \addtogroup Module_AgcTypes
  * \ref eDALProxyIrqLA640USBAGCProcessingValue is AGC Processing enum for ProxyIrqLA640USB_SetAGCProcessing and ProxyIrqLA640USB_GetAGCProcessing.
  *  @{ */

/** AGC types. */
DALProxyIrqLA640USB_API typedef enum
{
	eNoAGC =0,		/**< No AGC. */
	eAGCEqHisto,	/**< Histogram AGC. */
	eAGCLocal,		/**< Local AGC. */
	eAGCLinear,		/**< Linear AGC. */
	eAGCTotal
} eDALProxyIrqLA640USBAGCProcessingValue;

//! @}

/** \addtogroup Module_ErrFunc
  * \ref eDALProxyIrqLA640USBErr is returned by most functions as a result of execution.
  * \see eDALProxyIrqLA640USBErr() to convert code to user friendly string.
  *  @{ */

/** Code returned by most functions about execution. */
DALProxyIrqLA640USB_API typedef enum
{
    eProxyIrqLA640USBSuccess=0, /**< Function call success. */
    eProxyIrqLA640USBParameterError, /**< Function call with wrong parameter. */
    eProxyIrqLA640USBHandleError, /**< Function call with wrong or invalid Aion640 handle. */
    eProxyIrqLA640USBInitFailed,  /**< Internal error occur. */
    eProxyIrqLA640USBOpenFailed,  /**< Open connection to Aion640 failed. Maybe already connected */
    eProxyIrqLA640USBCommFailed,  /**< Exchange with Aion640 failed. */
    eProxyIrqLA640USBTimeout, /**< Operation on Aion640 timeout before completed. */
    eProxyIrqLA640USBSyncBroken, /**< GetImage(), Sync with Aion640 broken. */
    //
    eProxyIrqLA640USBSequencingError, /**< Function call outside correct sequencing */
    eProxyIrqLA640USBFeatureNotAvailable, /**< Feature not available on this module or can't be use due to present configuration. */
    eProxyIrqLA640USBBistInitFailure, /**< Built-In Self Test initialisation failed. */
    eProxyIrqLA640USBBistFailure, /**< Aion640 reported a Built-In Self Test error. */
    eProxyIrqLA640USBFormatFailed,  /**< Incompatible file format for Aion640. */
    //
    eProxyIrqLA640USBErrTotal
} eDALProxyIrqLA640USBErr;


/** Convert \ref eDALProxyIrqLA640USBErr to user message.
 * \param[in] paeError Function returns error code.
 * \return User error message from eDALProxyIrqLA640USBErr.
 * \note String is C-Style, i.e. Ascii with null terminate byte.
*/
DALProxyIrqLA640USB_API const char* ProxyIrqLA640USB_GetErrorString(eDALProxyIrqLA640USBErr paeError);

//! @}

/** \addtogroup Module_Management
 *
 * This set provides :
 * \li Functions to enumerates and name plugged Aion640.
 * \li Function to connect and disconnect to Aion640.
 *
 * Application call ProxyIrqLA640USB_GetModuleCount() to know how many Aion640 are plugged to workstation.
 * First Aion640 index is 0, and so on.
 *
 * Calling ProxyIrqLA640USB_GetModuleCount() check Aion640 count. So, call it will refresh Aion640 list.
 *
 * Before calling any other function's group, Application must connect to an Aion640 using ProxyIrqLA640USB_ConnectToModule().<br>
 * Once an Aion640 is connected by an application, it's not available to another application.
 * Application must release Aion640 by calling ProxyIrqLA640USB_DisconnectFromModule().
 *
 * Connection to Aion640 will provide a \em handle. This \em handle is used by all functions addressing this Aion640.
 * It remains valid until ProxyIrqLA640USB_DisconnectFromModule() is called.
 *
 * Application can connect several Aion640, using different \em handles.
* @{ */

/** Retrieve current count of plugged modules.
 * \param[out] paiCount Number of plugged modules.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetModuleCount(int* paiCount);

/** Query Aion640 name by index.
 * \param[in] iIdx Module index.
 * \param[out] paName Aion640 name from index.
 * \param[in] iLen paName storage size.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetModuleName(int iIdx, char* paName, int iLen);

/** Connect to Aion640 by index.<br>
 * This function will return a handle, which will be uses as Aion640 identifier.<br>
 * Connection may fail if Aion640 is already connected by another application.
 * \param[in] iIdx Module index. First Aion640 index is 0.
 * \param[out] paHandle Aion640 handle.
 * \param[in] bLoadDefaultFromModule if we load from the module.
 **/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_ConnectToModule(int iIdx, HANDLE* paHandle, bool bLoadDefaultFromModule);

/** Check if handle connection.
 * This function will check if handle is still valid, and then check connection with Aion640.
 * \param[in] paHandle Aion640 handle.
 *\return \ref eProxyIrqLA640USBSuccess on success, or error code.
 **/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_IsConnectToModule(HANDLE paHandle);

/** Disconnect to Aion640 by index.
 * This function will release Aion640 connection.
 * \param[in] paHandle Aion640 handle.
 **/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_DisconnectFromModule(HANDLE paHandle);

/** Run the Aion640 Built-In Self-Test.
 * This function will check if handle is still valid, and then run the built-in self tests.
 * \param[in] paHandle Aion640 handle.
 * \param[out] diagCode Diagnostic code provided by the Aion640. Value is 0 in case of success.
 * \return \ref eProxyIrqLA640USBSuccess on success, or error code.
 **/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_RunBIST(HANDLE paHandle, unsigned int *diagCode);

//! @}


/** \addtogroup Module_Image
 *
 * This set provides a single function to query current Aion640 image.
 * Calling it will block application until an image is available, or timeout occurs.
 *
 * Application may provide image storage for new IR image. Image nature (Raw or Fixed) depends on
 * processing settings (see \ref Module_Processing).
 *
 * IR image is <b>640 width by 512 height</b>. Pixel storage is unsigned short, with 16bit effective, LSB aligned.
 *
 * Along IR Image, some meta data are provided.
 *
 * @{ */
/** Query image from Aion640.
 * \param[in] paHandle Aion640 handle.
 * \param[out] paImage Image placeholder for new image. Must be at least <em>640 x 512 x 2= 640KB</em>.
 * \param[out] paMeta Meta-Data placeholder. Must be at least 269 16bit values :
 * \li [0] Reserved.
 * \li [1] bit 1 : Integration mode, 0 for ITR, 1 for IWR.
 * \li [1] bit 2 : IMRO enable (1) or disable (0).
 * \li [2] TFPA temperature in celsius (cast float to get it).
 * \li [3-7] Reserved.
 * \li [8] Frame counter (16bit effective).
 * \li [9] Missed trigger counter (16bit effective).
 * \li [10] IMRO counter (16bit effective).
 * \li [11-12] Microseconds since boot of the camera (32 bits).
 * \li [13-268] Histogram (128 * 32bits)
 * \param[in] paiTimeout Operation timeout in millisecond.
 *
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetImage(HANDLE paHandle, unsigned short* paImage, uint16_t *paMeta, int paiTimeout);

//! @}


/** \addtogroup Module_Control
 *
 *
 * @{ */

/** Query string feature.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paeFeature Feature requested.
 * \param[out] paStr String from requested feature.
 * \warning String Feature are 32 byte large, including null byte. Ensure paStr is large enougt.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetStringFeature(HANDLE paHandle, int paeFeature, char* paStr);

/** Query integer feature.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paeFeature Feature requested.
 * \param[out] paUInt Integer value from requested feature.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetUIntFeature(HANDLE paHandle, int paeFeature, unsigned int* paUInt);

/** Query float feature.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paeFeature Feature requested.
 * \param[out] paFloat Float value from requested feature.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetFloatFeature(HANDLE paHandle, int paeFeature, float* paFloat);


/** Set string feature.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paeFeature Feature written.
 * \param[in] paStr String for written feature.
 * \warning String Feature are 32 byte large, including null byte. Ensure paStr is large enougt.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetStringFeature(HANDLE paHandle, int paeFeature, const char* paStr);

/** Set integer feature.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paeFeature Feature written.
 * \param[in] paUInt Integer value for written feature.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetUIntFeature(HANDLE paHandle, int paeFeature, unsigned int paUInt);

/** Query float feature.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paeFeature Feature written.
 * \param[in] paFloat Float value for written feature.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetFloatFeature(HANDLE paHandle, int paeFeature, float paFloat);

//! @}

/** \addtogroup Module_Processing
 *
 * This set of function provides control over image processing.
 * \li Query and change processing step state (enable or disable).
 * \li Query processing parameters.
 * \li Set processing parameters.
 *
 * Processing is compose of :
 * \li Bad pixel correction.
 * \li Non linearity correction.
 *
 * \see <em>User's Guide</em> or \ref ProcessingChainPage for details
 *
 * @{ */

/** Enable/Disable NUC processing steps. These are enabled by default at connection.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paBadPixels Enable(1)/Disable(0) bad pixels correction.
 * \param[in] paNUC Enable(1)/Disable(0) Non Uniformity Correction.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetNUCProcessing(HANDLE paHandle, unsigned char paBadPixels, unsigned char paNUC);

/** Query NUC processing steps status.
 * \param[in] paHandle Aion640 handle.
 * \param[out] paBadPixels bad pixels correction enable(1) or disable(0).
 * \param[out] paNUC Non Uniformity Correction enable(1) or disable(0).
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetNUCProcessing(HANDLE paHandle, unsigned char* paBadPixels, unsigned char* paNUC);

/** Enable/Disable NUC processing steps. These are enabled by default at connection.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paBinning Binning disabled(0) 2x2(1) 4x4(2) 8x8(3) 16x16(4).
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetBinningProcessing(HANDLE paHandle, unsigned char paBinning);

/** Query NUC processing steps status.
 * \param[in] paHandle Aion640 handle.
 * \param[out] paBinning Binning disabled(0) 2x2(1) 4x4(2) 8x8(3) 16x16(4).
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetBinningProcessing(HANDLE paHandle, unsigned char* paBinning);

/** Set Auto Gain Control processing step. By default, No AGC processing set.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paeAGCProcessing see eDALProxyIrqLA640USBAGCProcessingValue for values.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetAGCProcessing(HANDLE paHandle, unsigned char paeAGCProcessing);

/** Query processing steps status.
 * \param[in] paHandle Aion640 handle.
 * \param[out] paeAGCProcessing see eDALProxyIrqLA640USBAGCProcessingValue for values.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetAGCProcessing(HANDLE paHandle, unsigned char* paeAGCProcessing);


/** Set some AGC local parameters.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paGlobalContrastStrength Global contrast strength [1-8].
 * \param[in] paLocalContrastStrength Local contrast strength [1-8].
 * \param[in] paSpeed Algorithm convergence speed [1-100]
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetCurrentAGCLocal(
    HANDLE       paHandle,
    float        paGlobalContrastStrength,
    float        paLocalContrastStrength,
    int          paSpeed
);


/** Set dark current regulation mode.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paDarkCurrent regulation mode (0 = none, 1 = looped, 2 = once).
 * \note When writing 1 or 2, a compensation is achieved.
 * \note The looped mode updates the dark current every 5 seconds.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetDarkCurrent(HANDLE paHandle, unsigned short paDarkCurrent);


/** Set dark current regulation settings.
 * \param[in] paHandle Aion640 handle.
 * \param[in] index Slot index to query.
 * \param[in] paDarknessValues New darkness values for darkness regulation
 * \note For maintenance only.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetDarkCurrentSettings(HANDLE paHandle, int index, double* paDarknessValues);


/** Reset dark current regulation settings.
 * \param[in] paHandle Aion640 handle.
 * \param[in] index Slot index to query.
 * \note For maintenance only.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_ResetDarkCurrentSettings(HANDLE paHandle, int index);


/** Set Gains values for NUC processing.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paTableGains New Gains values for NUC processing.
 * \note Each pixel must have a value. So paTableGains must contains 640 * 640 float values (4 bytes float).
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetCurrentTableGain(HANDLE paHandle, float* paTableGains);

/** Set Offset values for NUC processing.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paTableOffsets New offsets values for NUC processing.
 * \note Each pixel must have a value. So paTableOffsets must contains 640 * 512 values (2 bytes signed value).
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetCurrentTableOffset(HANDLE paHandle, signed short* paTableOffsets);

/** Set bad pixels position in image for bad pixels correction.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paTableX,paTableY Bad pixels position in image.
 * \param[in] paCount bad pixels count.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SetCurrentBadPixels(HANDLE paHandle, unsigned short *paTableX, unsigned short *paTableY,
                                             unsigned short paCount );


/** Get dark current regulation settings.
 * \param[in] paHandle Aion640 handle.
 * \param[in] index Slot index to query.
 * \param[out] paDarknessValues Darkness values for darkness regulation
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetDarkCurrentSettings(HANDLE paHandle, int index, double*& paDarknessValues);


/** Get Gains current values from NUC processing.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paTableGains Gains values for NUC processing.
 * \note Each pixel must have a value. So paTableGains must contains 640 * 512 float values (4 bytes float).
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetCurrentTableGain(HANDLE paHandle, float* paTableGains);

/** Get Offset current values from NUC processing.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paTableOffsets offsets values for NUC processing.
 * \note Each pixel must have a value. So  paTableOffsets must contains 640 * 512 values (2 bytes signed value).
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetCurrentTableOffset(HANDLE paHandle, signed short* paTableOffsets);

/** Get current bad pixels position in image from bad pixels correction.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paTableX,paTableY Bad pixels position in image.
 * \param paCount Initial bad pixels array size, on return, bad pixel count.
 * \note paCount must be init with  paTableX / paTableY placeholder size (to avoid overflow),
 * and will be modified by function with current bad pixel count.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_GetCurrentBadPixels(HANDLE paHandle, unsigned short *paTableX, unsigned short *paTableY,
                                             unsigned short *paCount );

//! @}

/** \addtogroup Module_Storage
 *  Aion640 provides \b 8 slots to store Gain or Offset value. Slot are not dedicated to a kind of data.
 *  \attention Storage space is limited into Aion640. Hence, data (Gain or Offset) are rounded to fit into slot.
 *  This may involve difference if your store data, read it, and compare to your initial values.
 *  For coherence, this data reduction is also apply when update NUC processing data (see \ref Module_Processing).
 *
 *  Save functions provides a \em MakeDefault parameter. When set to 1 (enable), this will mark slot as default.
 * When application connect to Aion640, ProxyIrqLA640USB_ConnectToModule() function will look for default slot,
 * and load into processing data from slot.
 @{ */

/** Default slot index for Gain values and Offset values, last setting's bank used.
 * \param[in] paHandle Aion640 handle.
 * \param[out] paiIdxGains Gain slot index, of 255 if no default Gain slot index.
 * \param[out] paiIdxOffsets Offset slot index, of 255 if no default Offset slot index.
 * \param[out] paiIdxBank Settings bank index, of 255 if no default settings index.
 * \note No need to call and use this function (already done at Aion640 connection)
 **/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_StartupDefault(HANDLE paHandle, unsigned char *paiIdxGains, unsigned char* paiIdxOffsets, unsigned char *paiIdxBank);

/** Query slot data type.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index to query.
 * \param[out] paeType Slot type.
 * \param[out] paData Table associate data. NULL, or 60 bytes placeholder. paData is additional data associated to Gain or Offset array, which can be used freely by application for instance to keep a trace of Gain or Offset table calibration conditions, either sensitivity, either focal plane array temperature.
 * Slot type value are :
 *\li 0 :Empty slot.
 *\li 1 :Gain values.
 *\li 2 :Offset values.
 **/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SlotType(HANDLE paHandle, unsigned char paiIndex, unsigned char* paeType,
                                                           void* paData);


/** Retrieve Aion640 slot data as Gain values.<br>
 * This function may failed if slot is empty, or slot data are not Gain values.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index as data.
 * \param[out] paTableGain Gain values from Aion640 slot.
 * \param[out] paData Table associate data. NULL, or 60 bytes placeholder. paData is additional data associated to Gain or Offset array, which can be used freely by application for instance to keep a trace of Gain or Offset table calibration conditions, either sensitivity, either focal plane array temperature.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_LoadTableGain(HANDLE paHandle, unsigned char paiIndex, float* paTableGain,
                                                                void* paData);

/** Retrieve Aion640 slot data as Offset values.<br>
 * This function may failed if slot is empty, or slot data are not Offset values.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index as data.
 * \param[out] paTableOffset Offset values from Aion640 slot.
 * \param[out] paData Table associate data. NULL, or 60 bytes placeholder. paData is additional data associated to Gain or Offset array, which can be used freely by application for instance to keep a trace of Gain or Offset table calibration conditions, either sensitivity, either focal plane array temperature.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_LoadTableOffset(HANDLE paHandle, unsigned char paiIndex, short* paTableOffset,
                                                                  void* paData);


/** Retrieve bad pixel position in image from Aion640.
 * \param[in] paHandle Aion640 handle.
 * \param[out] paTableX,paTableY Bad pixels position in image.
 * \param paCount Initial bad pixels array size, on return, bad pixel count.
 * \note paCount must be init with paTableX / paTableY placeholder size (to avoid overflow),
 * and will be modified by function with current bad pixel count.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_LoadBadPixels(HANDLE paHandle,
                                                                unsigned short *paTableX, unsigned short *paTableY,
                                                                unsigned short* paCount);


/** Save Gain values into Aion640 slot data.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index.
 * \param[in] paTableGain Gain values to store into Aion640 slot.
 * \param[in] paData Table associate data. NULL, or 60 bytes placeholder. paData is additional data associated to Gain or Offset array, which can be used freely by application for instance to keep a trace of Gain or Offset table calibration conditions, either sensitivity, either focal plane array temperature.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SaveTableGain(HANDLE paHandle, unsigned char paiIndex, const float* paTableGain,
                                              void* paData);

/** Save Offset values into Aion640 slot data.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index.
 * \param[in] paTableOffset Offset values to store into Aion640 slot.
 * \param[in] paData Table associate data. NULL, or 60 bytes placeholder. paData is additional data associated to Gain or Offset array, which can be used freely by application for instance to keep a trace of Gain or Offset table calibration conditions, either sensitivity, either focal plane array temperature.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SaveTableOffset(HANDLE paHandle, unsigned char paiIndex, const short* paTableOffset,
                                                                  void* paData);

/** Save bad pixel position into Aion640 slot data.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paTableX,paTableY Bad pixels position in image.
 * \param[in] paCount bad pixels count.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SaveBadPixels(HANDLE paHandle, const unsigned short *paTableX, const unsigned short* paTableY, unsigned short paCount);


/** Use Aion640 slot data as Gain values for NUC processing,
 * i.e. retrieve it from Aion640, and set it to NUC processing.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index as data.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_LoadCurrentTableGain(HANDLE paHandle, unsigned char paiIndex);

/** Use Aion640 slot data as Offset values for NUC processing,
 * i.e. retrieve it from Aion640, and set it to NUC processing.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index as data.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_LoadCurrentTableOffset(HANDLE paHandle, unsigned char paiIndex);

/** Use Aion640 stored bad pixel for bad pixel correction.
 * \param[in] paHandle Aion640 handle.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_LoadCurrentBadPixels(HANDLE paHandle);

/** Save current Gain values into Aion640 slot data.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index.
 * \param[in] paData Table associate data. NULL, or 60 bytes placeholder. paData is additional data associated to Gain or Offset array, which can be used freely by application for instance to keep a trace of Gain or Offset table calibration conditions, either sensitivity, either focal plane array temperature.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SaveCurrentTableGain(HANDLE paHandle, unsigned char paiIndex, const void *paData);

/** Save Offset values into Aion640 slot data.
 * \param[in] paHandle Aion640 handle.
 * \param[in] paiIndex Slot index.
 * \param[in] paData Table associate data. NULL, or 60 bytes placeholder. paData is additional data associated to Gain or Offset array, which can be used freely by application for instance to keep a trace of Gain or Offset table calibration conditions, either sensitivity, either focal plane array temperature.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SaveCurrentTableOffset(HANDLE paHandle, unsigned char paiIndex, const void *paData);

/** Save bad pixel position into Aion640 slot data.
 * \param[in] paHandle Aion640 handle.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_SaveCurrentBadPixels(HANDLE paHandle);



//! @}


/** \addtogroup Module_Calibration
 * This set of function provide 2 kinds of NUC calibrations :
 * \li 1Pt Calibration.
 * \li 2PTs Calibration.
 *
 * \see <em>User's Guide</em> or \ref CalibrationProcessPage for details.
* @{ */


/** Abort a Calibration process and reset the sequencing.
 * None of the corrections table will be change by the abort calibration.
 *
 * \param[in] paHandle Aion640 Handle.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_AbortCalibration(HANDLE paHandle);

/** Prepare NUC Calibration engine.
 * \param[in] paHandle Aion640 Handle.
 * \param[in] iStage Stage of the calibration (1 or 2).
 * \return eProxyIrqLA640USBSequencingError see \ref CalibrationProcessPage for details.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_Init2PtsCalibration(HANDLE paHandle, unsigned int iStage);

/** Add image for Shutter 2pts calibration.
  *
  * Low temperature image for iStage = 1, High temperature image for iStage = 2.
  *
  * \param[in] paHandle Aion640 Handle.
  * \param[in] iStage Stage of calibration (1 (low) or 2 (high)).
  * \return eProxyIrqLA640USBSequencingError see \ref CalibrationProcessPage for details.
  */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_Step2PtsCalibration(HANDLE paHandle, unsigned int iStage);

/** Perform two points calibration using low and high temperature images.
 *
 * Once calibration is done, new Gain, Offset and bad pixel are set to current NUC and BPC processing.
 *
 * \param[in] paHandle Aion640 handle.
 * \param[in] iStage Stage of the calibration. If stage = 2, perform the final step of calibration. Once is done, new Gain, Offset
 * and bad pixel are set to current NUC and BPC processing.
 * \return eProxyIrqLA640USBSequencingError see \ref CalibrationProcessPage for details.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_Finish2PtsCalibration(HANDLE paHandle,unsigned int iStage);

/** Prepare Shutter Calibration engine, also called one point calibration.
 *
 * This calibration will only produce new Offset values.
 *
 * \param[in] paHandle Aion640 handle.
 * \return eProxyIrqLA640USBSequencingError see \ref CalibrationProcessPage for details.
*/
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_Init1PtCalibration(HANDLE paHandle);

/** Add image to prepare Shutter Calibration
 *
 * \param[in] paHandle Aion640 handle.
 * \return eProxyIrqLA640USBSequencingError see \ref CalibrationProcessPage for details.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_Step1PtCalibration(HANDLE paHandle);

/** Perform Shutter calibration.
 *
 * Once calibration is done, Offset values are set to current NUC processing.
 *
 * \param[in] paHandle Aion640 handle.
 * \return eProxyIrqLA640USBSequencingError see \ref CalibrationProcessPage for details.
 */
DALProxyIrqLA640USB_API eDALProxyIrqLA640USBErr ProxyIrqLA640USB_Finish1PtCalibration(HANDLE paHandle);

//! @}



#ifdef __cplusplus
}
   }
#endif

#endif // __DALProxyIrqLA640USB_H__
