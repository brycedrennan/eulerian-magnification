# amplify_spatial_lpyr_temporal_iir(vidFile, resultsDir, ...
#                                   alpha, lambda_c, r1, r2, chromAttenuation)
#
# Spatial Filtering: Laplacian pyramid
# Temporal Filtering: substraction of two IIR lowpass filters
#
# y1[n] = r1*x[n] + (1-r1)*y1[n-1]
# y2[n] = r2*x[n] + (1-r2)*y2[n-1]
# (r1 > r2)
#
# y[n] = y1[n] - y2[n]
#
# Copyright (c) 2011-2012 Massachusetts Institute of Technology,
# Quanta Research Cambridge, Inc.
#
# Authors: Hao-yu Wu, Michael Rubinstein, Eugene Shih,
# License: Please refer to the LICENCE file
# Date: June 2012
#
@mfunction("")
def amplify_spatial_lpyr_temporal_iir(vidFile=None, resultsDir=None, alpha=None, lambda_c=None, r1=None, r2=None, chromAttenuation=None):

    fileparts(vidFile)
    num2str(alpha)
    mstring('-lambda_c-')
    num2str(lambda_c)
    mstring('-chromAtn-')
    num2str(chromAttenuation)

    # Read video
    vid = VideoReader(vidFile)
    # Extract video info
    vidHeight = vid.Height
    vidWidth = vid.Width
    nChannels = 3
    fr = vid.FrameRate
    len = vid.NumberOfFrames
    temp = struct(mstring('cdata'), zeros(vidHeight, vidWidth, nChannels, mstring('uint8')), mstring('colormap'), mcat([]))


    startIndex = 1
    endIndex = len - 10

    vidOut = VideoWriter(outName)
    vidOut.FrameRate = fr

    open(vidOut)

    # firstFrame
    temp.cdata = read(vid, startIndex)
    frame2im(temp)
    rgbframe = im2double(rgbframe)
    frame = rgb2ntsc(rgbframe)

    [pyr, pind] = buildLpyr(frame(mslice[:], mslice[:], 1), mstring('auto'))
    pyr = repmat(pyr, mcat([1, 3]))
    buildLpyr(frame(mslice[:], mslice[:], 2), mstring('auto'))
    buildLpyr(frame(mslice[:], mslice[:], 3), mstring('auto'))

    lowpass1 = pyr
    lowpass2 = pyr

    output = rgbframe
    writeVideo(vidOut, im2uint8(output))

    nLevels = size(pind, 1)

    for i in mslice[startIndex + 1:endIndex]:



        temp.cdata = read(vid, i)
        frame2im(temp)

        rgbframe = im2double(rgbframe)
        frame = rgb2ntsc(rgbframe)

        buildLpyr(frame(mslice[:], mslice[:], 1), mstring('auto'))
        buildLpyr(frame(mslice[:], mslice[:], 2), mstring('auto'))
        buildLpyr(frame(mslice[:], mslice[:], 3), mstring('auto'))

        # temporal filtering
        lowpass1 = (1 - r1) * lowpass1 + r1 * pyr
        lowpass2 = (1 - r2) * lowpass2 + r2 * pyr

        filtered = (lowpass1 - lowpass2)


        #% amplify each spatial frequency bands according to Figure 6 of our paper
        ind = size(pyr, 1)

        delta = lambda_c / 8 / (1 + alpha)

        # the factor to boost alpha above the bound we have in the
        # paper. (for better visualization)
        exaggeration_factor = 2

        # compute the representative wavelength lambda for the lowest spatial
        # freqency band of Laplacian pyramid

        _lambda = (vidHeight ** 2 + vidWidth ** 2) **elpow** 0.5 / 3    # 3 is experimental constant

        for l in mslice[nLevels:-1:1]:
            indices = mslice[ind - prod(pind(l, mslice[:])) + 1:ind]
            # compute modified alpha for this level
            currAlpha = _lambda / delta / 8 - 1
            currAlpha = currAlpha * exaggeration_factor

            if (l == nLevels or l == 1):            # ignore the highest and lowest frequency band
                filtered(indices, mslice[:]).lvalue = 0
            elif (currAlpha > alpha):            # representative lambda exceeds lambda_c
                filtered(indices, mslice[:]).lvalue = alpha * filtered(indices, mslice[:])
            else:
                filtered(indices, mslice[:]).lvalue = currAlpha * filtered(indices, mslice[:])
            end

            ind = ind - prod(pind(l, mslice[:]))
            # go one level down on pyramid,
            # representative lambda will reduce by factor of 2
            _lambda = _lambda / 2
        end


        #% Render on the input video
        output = zeros(size(frame))

        output(mslice[:], mslice[:], 1).lvalue = reconLpyr(filtered(mslice[:], 1), pind)
        output(mslice[:], mslice[:], 2).lvalue = reconLpyr(filtered(mslice[:], 2), pind)
        output(mslice[:], mslice[:], 3).lvalue = reconLpyr(filtered(mslice[:], 3), pind)

        output(mslice[:], mslice[:], 2).lvalue = output(mslice[:], mslice[:], 2) * chromAttenuation
        output(mslice[:], mslice[:], 3).lvalue = output(mslice[:], mslice[:], 3) * chromAttenuation

        output = frame + output

        output = ntsc2rgb(output)
        #             filtered = rgbframe + filtered.*mask;

        output(output > 1).lvalue = 1
        output(output < 0).lvalue = 0

        writeVideo(vidOut, im2uint8(output))



    end
    close(vidOut)
end