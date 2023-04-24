🛠️ File analysis in progress 🛠️

Blender Addon to create and manipulate shp0 files, used for polygon morphing and vertex displacement animations.
Reverse engineering process to understand the .shp0 file format from hex.


    roadmap:
        + is done
        * partially done
        - needs to be done

        Priorities:
            verify is animation data/entry correctly written to file
            section 1
            update offsets

        
        section 0:
            file header (just need length of file update with                                           +
            ftell() then fseek(0x04) once all the file is written)
            
            shp0 header                                                                                 +
        
            Animation Data
                use of shape keys for animation entries
                0x00 bitflags                                                                           +
                (but still need the update animation button, hopefully find a way to get rid of it)
                and better coord between vg size and animIndex (off by 1 when size vg -1)               *
                
                0x04/8? name offset to section one vg name                                              *
                0x0A number of shape keys   (len(bpy.types.ShapeKey))                                   *
                
                0x0C-0x10-0x14 TBD                                                                      -
            
            Animation Entry
                "header"
                    this shape key number of kf                                                         +
                    padding                                                                             -
                    1/(max kf number)                                                                   +
                followed by kf entries: (size N*12)
                    frame number                                                                        +
                    shape key animation value (0-1 morph)                                               +
                    interpolation tangent value (f-curve or shapeKey.interpolation data struct?)        *
                    
        section 1:
            list of vertex group names                                                                  -