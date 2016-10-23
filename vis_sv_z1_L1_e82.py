#!/usr/bin/env python

import sys, traceback
import cv2
import os
import re
import numpy as np
import argparse
import string
import plantcv as pcv


def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r","--result", help="result file.", required= False )
    parser.add_argument("-w","--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action=None)
    args = parser.parse_args()
    return args

### Main pipeline
def main():
  # Get options
  args = options()
  
  # Read image
  img, path, filename = pcv.readimage(args.image)
    
  # Pipeline step
  device = 0

  # Convert RGB to HSV and extract the Saturation channel
  device, s = pcv.rgb2gray_hsv(img, 's', device, args.debug)
  
  # Threshold the Saturation image
  device, s_thresh = pcv.binary_threshold(s, 30, 255, 'light', device, args.debug)
  
  # Median Filter
  device, s_mblur = pcv.median_blur(s_thresh, 5, device, args.debug)
  
  # Convert RGB to LAB and extract the Blue channel
  device, b = pcv.rgb2gray_lab(img, 'b', device, args.debug)
  
  # Threshold the blue image
  device, b_thresh = pcv.binary_threshold(b, 132, 255, 'light', device, args.debug)

  # Join the thresholded saturation and blue-yellow images
  device, bs = pcv.logical_or(s_mblur, b_thresh, device, args.debug)
  
  # Apply Mask (for vis images, mask_color=white)
  device, masked = pcv.apply_mask(img, bs, 'white', device, args.debug)
  
  # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
  device, masked_a = pcv.rgb2gray_lab(masked, 'a', device, args.debug)
  device, masked_b = pcv.rgb2gray_lab(masked, 'b', device, args.debug)
  
  # Threshold the green-magenta and blue images
  device, maskeda_thresh = pcv.binary_threshold(masked_a, 125, 255, 'dark', device, args.debug)
  device, maskedb_thresh = pcv.binary_threshold(masked_b, 135, 255, 'light', device, args.debug)
  
  # Join the thresholded saturation and blue-yellow images (OR)
  device, ab = pcv.logical_and(maskeda_thresh, maskedb_thresh, device, args.debug)
  device, ab_cnt = pcv.logical_and(maskeda_thresh, maskedb_thresh, device, args.debug)
  
  # Fill small noise
  device, ab_fill1 = pcv.fill(ab, ab_cnt, 300, device, args.debug)
  device, masked2 = pcv.apply_mask(masked, ab_fill1, 'white', device, args.debug)

  # Identify objects
  device, id_objects,obj_hierarchy = pcv.find_objects(masked2, ab_fill1, device, args.debug)
  
  # Define ROI
  device, roi1, roi_hierarchy= pcv.define_roi(masked2,'rectangle', device, None, 'default', args.debug,True, 600, 0,-600,-375)
  
  # Decide which objects to keep
  device,roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img,'partial',roi1,roi_hierarchy,id_objects,obj_hierarchy,device, args.debug)
  
  # Object combine kept objects
  device, obj, mask = pcv.object_composition(img, roi_objects, hierarchy3, device, args.debug)
  
  ############## VIS Analysis ################
  
  outfile=False
  if args.writeimg==True:
    outfile=args.outdir+"/"+filename
  
  # Find shape properties, output shape image (optional)
  device, shape_header,shape_data,shape_img = pcv.analyze_object(img, args.image, obj, mask, device,args.debug,outfile)
  
  # Shape properties relative to user boundary line (optional)
  device, boundary_header,boundary_data, boundary_img1= pcv.analyze_bound(img, args.image,obj, mask, 384, device,args.debug,outfile)
  
  # Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
  device, color_header,color_data,color_img= pcv.analyze_color(img, args.image, mask, 256, device, args.debug,None,'v','img',300,outfile)
  
  # Output shape and color data
  result=open(args.result,"a")
  result.write('\t'.join(map(str,shape_header)))
  result.write("\n")
  result.write('\t'.join(map(str,shape_data)))
  result.write("\n")
  for row in shape_img:
    result.write('\t'.join(map(str,row)))
    result.write("\n")
  result.write('\t'.join(map(str,color_header)))
  result.write("\n")
  result.write('\t'.join(map(str,color_data)))
  result.write("\n")
  result.write('\t'.join(map(str,boundary_header)))
  result.write("\n")
  result.write('\t'.join(map(str,boundary_data)))
  result.write("\n")
  result.write('\t'.join(map(str,boundary_img1)))
  result.write("\n")
  for row in color_img:
    result.write('\t'.join(map(str,row)))
    result.write("\n")
  result.close()

if __name__ == '__main__':
  main()

