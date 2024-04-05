run bash setup.sh from project root

Some file changes are required for the build to function. These are handled in setup.sh.

1. Pangolin/CMakeModules/FindFFMPEG.cmake
- line #63, 64
FROM
  sizeof(AVFormatContext::max_analyze_duration2);
}" HAVE_FFMPEG_MAX_ANALYZE_DURATION2
TO
  sizeof(AVFormatContext::max_analyze_duration);
}" HAVE_FFMPEG_MAX_ANALYZE_DURATION

2. Pangolin/src/video/drivers/ffmpeg.cpp
- line #37
ADD
#define CODEC_FLAG_GLOBAL_HEADER AV_CODEC_FLAG_GLOBAL_HEADER

- line #78, 79
FROM
	TEST_PIX_FMT_RETURN(XVMC_MPEG2_MC);
	TEST_PIX_FMT_RETURN(XVMC_MPEG2_IDCT);

TO
#ifdef FF_API_XVMC
	TEST_PIX_FMT_RETURN(XVMC_MPEG2_MC);
	TEST_PIX_FMT_RETURN(XVMC_MPEG2_IDCT);
#endif

- line #101-105
FROM
	TEST_PIX_FMT_RETURN(VDPAU_H264);
	TEST_PIX_FMT_RETURN(VDPAU_MPEG1);
	TEST_PIX_FMT_RETURN(VDPAU_MPEG2);
	TEST_PIX_FMT_RETURN(VDPAU_WMV3);
	TEST_PIX_FMT_RETURN(VDPAU_VC1);

TO
#ifdef FF_API_VDPAU
	TEST_PIX_FMT_RETURN(VDPAU_H264);
	TEST_PIX_FMT_RETURN(VDPAU_MPEG1);
	TEST_PIX_FMT_RETURN(VDPAU_MPEG2);
	TEST_PIX_FMT_RETURN(VDPAU_WMV3);
	TEST_PIX_FMT_RETURN(VDPAU_VC1);
#endif

- line #127
FROM
	TEST_PIX_FMT_RETURN(VDPAU_MPEG4);

TO
#ifdef FF_API_VDPAU
	TEST_PIX_FMT_RETURN(VDPAU_MPEG4);
#endif

3. Pangolin/include/pangolin/video/drivers/ffmpeg.h
- line #53
ADD
#define AV_CODEC_FLAG_GLOBAL_HEADER (1 << 22)
#define CODEC_FLAG_GLOBAL_HEADER AV_CODEC_FLAG_GLOBAL_HEADER
#define AVFMT_RAWPICTURE 0x0020

4. Pangolin/src/display/device/display_x11.cpp
- line #115
### THIS ONE BREAKS THE BUILD DO NOT USE ###
FROM
GLXFBConfig* fbc = glXChooseFBConfig(display, DefaultScreen(display), visual_attribs, &fbcount);

TO
// GLXFBConfig* fbc = glXChooseFBConfig(display, DefaultScreen(display), visual_attribs, &fbcount);
cm

- line #177
FROM
{
	throw std::runtime_error("Pangolin in X11: ...");
}

TO
{
	// throw std::runtime_error("Pangolin in X11: ...");
}

5. In order to prevent "double free or corruption" error, need to patch ORB_SLAM2 for march native building 
wget https://gist.githubusercontent.com/matlabbe/c10403c5d44af85cc3585c0e1c601a60/raw/48adf04098960d86ddf225f1a8c68af87bfcf56e/orbslam2_f2e6f51_marchnative_disabled.patch
git apply orbslam2_f2e6f51_marchnative_disabled.patch

6. How to prevent "EIGEN_DEPRECATED const unsigned int AlignedBit = 0x80;" warning in build?
