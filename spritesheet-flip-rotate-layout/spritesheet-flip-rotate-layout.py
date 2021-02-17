#!/usr/bin/env python

from gimpfu import *

def SPRITESHEET_FLIP_ROTATE_LAYOUT(image, drawable, spriteWidth, spriteHeight, padding, paddingColor, columns, rows):
	pdb.gimp_message("spriteWidth = " + str(spriteWidth))
	pdb.gimp_message("spriteHeight = " + str(spriteHeight))
	pdb.gimp_message("padding = " + str(padding))
	pdb.gimp_image_undo_group_start(image)
	# Resize image canvas
	newWidth = (image.width * 2) + padding
	newheight = image.height
	pdb.gimp_image_resize(image, newWidth, newheight, 0, 0)
	pdb.gimp_layer_resize_to_image_size(image.layers[0])
	# Draw padding grid (if required)
	if(padding > 0):
		for x in range(1, int(columns) * 2):
			startX = (spriteWidth * x) + x - 1
			startY = 0
			endX = (spriteWidth * x) + x - 1
			endY = image.height
			DrawPaddingLine(image, startX, startY, endX, endY, paddingColor)
			pdb.gimp_message("(" + str(startX) + "," + str(startY) + "), (" + str(endX) + ", " + str(endY) + ")")
		for y in range(1, int(rows)):
			startX = 0
			startY = (spriteHeight * y) + y - 1
			endX = image.width
			endY = (spriteHeight * y) + y - 1
			DrawPaddingLine(image, startX, startY, endX, endY, paddingColor)
			pdb.gimp_message("(0," + str(spriteHeight * y) + "), (" + str(image.width) + ", " + str(spriteHeight * y) + ")")
	
	# Loop through all sprites and individually apply the transformation to them
	for x in range(0, int(columns)):
		for y in range(0, int(rows)):
			pdb.gimp_message("x=" + str(x) + ", y=" + str(y))
			startTopLeftCoordX = (spriteWidth * x) + (padding * x)
			startTopLeftCoordY = (spriteHeight * y) + (padding * y)
			endOffsetX = (spriteWidth * columns) + (padding * columns)
			endOffsetY = 0
			pdb.gimp_message(str(endOffsetY))
			ApplyTransformation(image, drawable, spriteWidth, spriteHeight, startTopLeftCoordX, startTopLeftCoordY, endOffsetX, endOffsetY)
	
	pdb.gimp_image_undo_group_end(image)


def DrawPaddingLine(image, startX, startY, endX, endY, paddingColor):
	brushName = pdb.gimp_brush_new("PaddingBrush")
	pdb.gimp_context_set_foreground(paddingColor)
	pdb.gimp_context_set_brush(brushName)
	pdb.gimp_context_set_opacity(100)
	pdb.gimp_context_set_brush_angle(0.0)
	pdb.gimp_context_set_brush_aspect_ratio(0.0)
	pdb.gimp_context_set_brush_force(1.0)
	pdb.gimp_context_set_brush_hardness(1.0)
	pdb.gimp_context_set_brush_size(1.0)
	pdb.gimp_pencil(image.layers[0], 4, [startX, startY, endX, endY])


def ApplyTransformation(image, drawable, spriteWidth, spriteHeight, startTopLeftCoordX, startTopLeftCoordY, endOffsetX, endOffsetY):
	# Get bottom-left sprite based on passed values
	selectionOperation = 2
	pdb.gimp_image_select_rectangle(image, selectionOperation, startTopLeftCoordX, startTopLeftCoordY, spriteWidth, spriteHeight)
	selection = pdb.gimp_selection_bounds(image)
	pdb.gimp_message(selection)
	# Duplicate selected area into new layer
	pdb.gimp_edit_copy(drawable)
	pasteInto = 0
	floatingSelection = pdb.gimp_edit_paste(drawable, pasteInto)
	# Translate
	pdb.gimp_layer_translate(floatingSelection, endOffsetX, endOffsetY)
	# Flip
	flipType = 0
	autoCentre = True
	axis = 0.0
	flippedItem = pdb.gimp_item_transform_flip_simple(floatingSelection, flipType, autoCentre, axis)
	# Rotate
	rotateType = 2
	centerX = 0
	centerY = 0
	rotatedItem = pdb.gimp_item_transform_rotate_simple(flippedItem, rotateType, autoCentre, centerX, centerY)
	# Anchor floating selection to drawable
	pdb.gimp_floating_sel_anchor(rotatedItem)



register(
    "SPRITESHEET-FLIP-ROTATE-LAYOUT",
    "Flip, rotate, and layout a spritesheet according to certain set parameters",
    "LONG DESCRIPTION",
    "Rob Willson", "RF", "2021",
    "Flip & Rotate",
    "RGB*", # type of image it works on (*, RGB, RGB*, RGBA, GRAY etc...)
    [
        # basic parameters are: (UI_ELEMENT, "variable", "label", Default)
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "Input layer", None),
        (PF_SLIDER, "spriteWidth", "Sprite width", 64, (32, 128, 32)),
        (PF_SLIDER, "spriteHeight", "Sprite height", 64, (32, 128, 32)),
        (PF_SLIDER, "padding", "Padding", 0, (0, 1, 1)),
        (PF_COLOR, "paddingColor", "Padding color", (255, 0, 255)),
        (PF_SLIDER, "columns", "Columns", 1, (1, 20, 1)),
        (PF_SLIDER, "rows", "Rows", 1, (1, 20, 1))
    ],
    [],
    SPRITESHEET_FLIP_ROTATE_LAYOUT, menu="<Image>/Tools/Spritesheets")  # second item is menu location

main()