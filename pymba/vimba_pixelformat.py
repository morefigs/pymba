from enum import IntFlag

#
# Translation of the enum data types from the original VmbCommonTypes.h header file
#


class VmbPixel(IntFlag):
    # Indicate if pixel is monochrome or RGB.
    Mono  = 0x01000000  # Monochrome pixel
    Color = 0x02000000  # Pixel bearing color information

    # Indicate number of bits for a pixel. Needed for building values of VmbPixelFormatType
    Occupy8Bit  = 0x00080000  # Pixel effectively occupies 8 bits
    Occupy10Bit = 0x000A0000  # Pixel effectively occupies 10 bits
    Occupy12Bit = 0x000C0000  # Pixel effectively occupies 12 bits
    Occupy14Bit = 0x000E0000  # Pixel effectively occupies 14 bits
    Occupy16Bit = 0x00100000  # Pixel effectively occupies 16 bits
    Occupy24Bit = 0x00180000  # Pixel effectively occupies 24 bits
    Occupy32Bit = 0x00200000  # Pixel effectively occupies 32 bits
    Occupy48Bit = 0x00300000  # Pixel effectively occupies 48 bits
    Occupy64Bit = 0x00400000  # Pixel effectively occupies 48 bits


class VmbPixelFormat(IntFlag):
    # Pixel format types.
    # As far as possible, the Pixel Format Naming Convention (PFNC) has been followed, allowing a
    # few deviations.
    # If data spans more than one byte, it is always LSB aligned, except if stated differently.

    # mono formats
    Mono8        = VmbPixel.Mono | VmbPixel.Occupy8Bit  | 0x0001  # Monochrome, 8 bits(PFNC: Mono8)
    Mono10       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0003  # Monochrome, 10 bits in 16 bits(PFNC: Mono10)
    Mono10p      = VmbPixel.Mono | VmbPixel.Occupy10Bit | 0x0046  # Monochrome, 10 bits in 16 bits(PFNC: Mono10p)
    Mono12       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0005  # Monochrome, 12 bits in 16 bits(PFNC: Mono12)
    Mono12Packed = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x0006  # Monochrome, 2x12 bits in 24 bits(GEV: Mono12Packed)
    Mono12p      = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x0047  # Monochrome, 2x12 bits in 24 bits(PFNC: MonoPacked)
    Mono14       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0025  # Monochrome, 14 bits in 16 bits(PFNC: Mono14)
    Mono16       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0007  # Monochrome, 16 bits(PFNC: Mono16)

    # bayer formats
    BayerGR8        = VmbPixel.Mono | VmbPixel.Occupy8Bit  | 0x0008  # Bayer - color, 8 bits, starting with GR line (PFNC:BayerGR8)
    BayerRG8        = VmbPixel.Mono | VmbPixel.Occupy8Bit  | 0x0009  # Bayer - color, 8 bits, starting with RG line (PFNC:BayerRG8)
    BayerGB8        = VmbPixel.Mono | VmbPixel.Occupy8Bit  | 0x000A  # Bayer - color, 8 bits, starting with GB line (PFNC:BayerGB8)
    BayerBG8        = VmbPixel.Mono | VmbPixel.Occupy8Bit  | 0x000B  # Bayer - color, 8 bits, starting with BG line (PFNC:BayerBG8)
    BayerGR10       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x000C  # Bayer - color, 10 bits in 16 bits, starting with GR line (PFNC:BayerGR10)
    BayerRG10       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x000D  # Bayer - color, 10 bits in 16 bits, starting with RG line (PFNC:BayerRG10)
    BayerGB10       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x000E  # Bayer - color, 10 bits in 16 bits, starting with GB line (PFNC:BayerGB10)
    BayerBG10       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x000F  # Bayer - color, 10 bits in 16 bits, starting with BG line (PFNC:BayerBG10)
    BayerGR12       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0010  # Bayer - color, 12 bits in 16 bits, starting with GR line (PFNC:BayerGR12)
    BayerRG12       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0011  # Bayer - color, 12 bits in 16 bits, starting with RG line (PFNC:BayerRG12)
    BayerGB12       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0012  # Bayer - color, 12 bits in 16 bits, starting with GB line (PFNC:BayerGB12)
    BayerBG12       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0013  # Bayer - color, 12 bits in 16 bits, starting with BG line (PFNC:BayerBG12)
    BayerGR12Packed = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x002A  # Bayer - color, 2 x12 bits in 24 bits, starting with GR line (GEV:BayerGR12Packed)
    BayerRG12Packed = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x002B  # Bayer - color, 2 x12 bits in 24 bits, starting with RG line (GEV:BayerRG12Packed)
    BayerGB12Packed = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x002C  # Bayer - color, 2 x12 bits in 24 bits, starting with GB line (GEV:BayerGB12Packed)
    BayerBG12Packed = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x002D  # Bayer - color, 2 x12 bits in 24 bits, starting with BG line (GEV:BayerBG12Packed)
    BayerGR10p      = VmbPixel.Mono | VmbPixel.Occupy10Bit | 0x0056  # Bayer - color, 12 bits continuous packed, starting with GR line (PFNC:BayerGR10p)
    BayerRG10p      = VmbPixel.Mono | VmbPixel.Occupy10Bit | 0x0058  # Bayer - color, 12 bits continuous packed, starting with RG line (PFNC:BayerRG10p)
    BayerGB10p      = VmbPixel.Mono | VmbPixel.Occupy10Bit | 0x0054  # Bayer - color, 12 bits continuous packed, starting with GB line (PFNC:BayerGB10p)
    BayerBG10p      = VmbPixel.Mono | VmbPixel.Occupy10Bit | 0x0052  # Bayer - color, 12 bits continuous packed, starting with BG line (PFNC:BayerBG10p)
    BayerGR12p      = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x0057  # Bayer - color, 12 bits continuous packed, starting with GR line (PFNC:BayerGR12p)
    BayerRG12p      = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x0059  # Bayer - color, 12 bits continuous packed, starting with RG line (PFNC:BayerRG12p)
    BayerGB12p      = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x0055  # Bayer - color, 12 bits continuous packed, starting with GB line (PFNC:BayerGB12p)
    BayerBG12p      = VmbPixel.Mono | VmbPixel.Occupy12Bit | 0x0053  # Bayer - color, 12 bits continuous packed, starting with BG line (PFNC:BayerBG12p)
    BayerGR16       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x002E  # Bayer - color, 16 bits, starting with GR line (PFNC:BayerGR16)
    BayerRG16       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x002F  # Bayer - color, 16 bits, starting with RG line (PFNC:BayerRG16)
    BayerGB16       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0030  # Bayer - color, 16 bits, starting with GB line (PFNC:BayerGB16)
    BayerBG16       = VmbPixel.Mono | VmbPixel.Occupy16Bit | 0x0031  # Bayer - color, 16 bits, starting with BG line (PFNC:BayerBG16)

    # rgb formats
    Rgb8   = VmbPixel.Color | VmbPixel.Occupy24Bit | 0x0014  # RGB, 8 bits x 3(PFNC: RGB8)
    Bgr8   = VmbPixel.Color | VmbPixel.Occupy24Bit | 0x0015  # BGR, 8 bits x 3(PFNC: BGR8)
    Rgb10  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x0018  # RGB, 12 bits in 16 bits x 3(PFNC: RGB12)
    Bgr10  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x0019  # RGB, 12 bits in 16 bits x 3(PFNC: RGB12)
    Rgb12  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x001A  # RGB, 12 bits in 16 bits x 3(PFNC: RGB12)
    Bgr12  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x001B  # RGB, 12 bits in 16 bits x 3(PFNC: RGB12)
    Rgb14  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x005E  # RGB, 14 bits in 16 bits x 3(PFNC: RGB12)
    Bgr14  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x004A  # RGB, 14 bits in 16 bits x 3(PFNC: RGB12)
    Rgb16  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x0033  # RGB, 16 bits x 3(PFNC: RGB16)
    Bgr16  = VmbPixel.Color | VmbPixel.Occupy48Bit | 0x004B  # RGB, 16 bits x 3(PFNC: RGB16)

    # rgba formats
    Argb8  = VmbPixel.Color | VmbPixel.Occupy32Bit | 0x0016  # ARGB, 8 bits x 4(PFNC: RGBa8)
    Rgba8  = VmbPixel.Color | VmbPixel.Occupy32Bit | 0x0016  # RGBA, 8 bits x 4, legacy name, same as Argb8
    Bgra8  = VmbPixel.Color | VmbPixel.Occupy32Bit | 0x0017  # BGRA, 8 bits x 4(PFNC: BGRa8)
    Rgba10 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x005F  # RGBA, 8 bits x 4, legacy name
    Bgra10 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x004C  # RGBA, 8 bits x 4, legacy name
    Rgba12 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x0061  # RGBA, 8 bits x 4, legacy name
    Bgra12 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x004E  # RGBA, 8 bits x 4, legacy name
    Rgba14 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x0063  # RGBA, 8 bits x 4, legacy name
    Bgra14 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x0050  # RGBA, 8 bits x 4, legacy name
    Rgba16 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x0064  # RGBA, 8 bits x 4, legacy name
    Bgra16 = VmbPixel.Color | VmbPixel.Occupy64Bit | 0x0051  # RGBA, 8 bits x 4, legacy name

    # yuv / ycbcr formats
    Yuv411              = VmbPixel.Color | VmbPixel.Occupy12Bit | 0x001E  # YUV 411 with 8 bits (GEV:YUV411Packed)
    Yuv422              = VmbPixel.Color | VmbPixel.Occupy16Bit | 0x001F  # YUV 422 with 8 bits (GEV:YUV422Packed)
    Yuv444              = VmbPixel.Color | VmbPixel.Occupy24Bit | 0x0020  # YUV 444 with 8 bits (GEV:YUV444Packed)
    YCbCr411_8_CbYYCrYY = VmbPixel.Color | VmbPixel.Occupy12Bit | 0x003C  # Y'CbCr 411 with 8 bits (PFNC:YCbCr411_8_CbYYCrYY) - identical to Yuv411
    YCbCr422_8_CbYCrY   = VmbPixel.Color | VmbPixel.Occupy16Bit | 0x0043  # Y'CbCr 422 with 8 bits (PFNC:YCbCr422_8_CbYCrY) - identical to Yuv422
    YCbCr8_CbYCr        = VmbPixel.Color | VmbPixel.Occupy24Bit | 0x003A  # Y'CbCr 444 with 8 bits (PFNC:YCbCr8_CbYCr) - identical to Yuv444