# Before running this scipt, open mickey.blend.
# Vector comes with mathutils.
import mathutils
# Set Camera object to a variable.
cam = bpy.dataobjects['Camera']

# Loop to create images from different perspectives.
for counter in range(0,18):
    # Angle is calculated according to counter.
    alpha = 5*counter
    # Radius of the circle.
    h     = -1.1
    # Coordinates for the new camera location.
    x     = sin(radians(-alpha))*h; y= cos(radians(alpha))*h; z= 0
    # Set Camera location.
    cam.location = (x,y,z)
    # Camera rotation is set accordingly to new location.
    cam.rotation_euler = (pi/2-radians(alpha),pi/2,0)
    # Determines where to save image.
    bpy.data.scenes['Scene'].render.filepath = '/home/kaan/image%s.jpg' % counter
    # Renders image.
    bpy.ops.render.render(write_still=True)
    # Increment counter.
    counter += 1
