import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel

WINDOW_NAME = "autoSkirtWindow"


class AutoSkirtUI(object):

    def __init__(self):
        self.garment_mesh = None
        self.guide_vertices = []
        self.collider = None
        self.collider_driver_joints = []
        self.collider_skin_source = None

        # -------------------------------------------------
        # Manual CTRL colors per section
        # -------------------------------------------------

        self.ctrl_colors = {
            "front_L": (0.25, 0.55, 1.0),
            "front_R": (1.0, 0.30, 0.30),
            "side_L": (0.25, 0.55, 1.0),
            "side_R": (1.0, 0.30, 0.30),
            "back_L": (0.25, 0.55, 1.0),
            "back_R": (1.0, 0.30, 0.30)
        }

        # Az ordered vertex selection kell az AutoSkirthöz.
        if not cmds.selectPref(q=True, trackSelectionOrder=True):
            cmds.selectPref(trackSelectionOrder=True)

        self.build_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def build_ui(self):

        if cmds.window(WINDOW_NAME, exists=True):
            cmds.deleteUI(WINDOW_NAME)

        self.window = cmds.window(
            WINDOW_NAME,
            title="AutoSkirt",
            widthHeight=(420, 650),
            sizeable=True
        )

        cmds.scrollLayout(
            childResizable=True,
            horizontalScrollBarThickness=0
        )

        cmds.columnLayout(
            adjustableColumn=True,
            rowSpacing=8,
            columnOffset=("both", 12)
        )

        # -----------------------------------------------------
        # 1. GUIDE SETUP
        # -----------------------------------------------------

        cmds.separator(height=3, style="none")

        cmds.text(
            label="1. GUIDE SETUP",
            align="left",
            font="boldLabelFont"
        )

        cmds.separator(height=3, style="in")

        # Garment Mesh
        cmds.text(
            label="Garment Mesh",
            align="left"
        )

        cmds.rowLayout(
            numberOfColumns=2,
            adjustableColumn=1,
            columnWidth2=(320, 70),
            columnAttach=[
                (1, "both", 0),
                (2, "left", 6)
            ]
        )

        self.mesh_field = cmds.textField(
            editable=False,
            placeholderText="Select garment mesh..."
        )

        cmds.button(
            label="Set",
            width=70,
            command=self.set_garment_mesh
        )

        cmds.setParent("..")

        # Section
        cmds.separator(height=6, style="none")

        cmds.text(
            label="Section",
            align="left"
        )

        self.section_menu = cmds.optionMenu()

        cmds.menuItem(label="Front Left")
        cmds.menuItem(label="Front Right")
        cmds.menuItem(label="Left Side")
        cmds.menuItem(label="Right Side")
        cmds.menuItem(label="Back Left")
        cmds.menuItem(label="Back Right")

        cmds.optionMenu(
            self.section_menu,
            edit=True,
            changeCommand=self.update_ctrl_color_picker
        )

        # Selection information
        cmds.separator(height=12, style="none")

        cmds.text(
            label="Select consecutive vertices from START to END.",
            align="left"
        )

        self.selection_info = cmds.text(
            label="Selected Guide Points: 0    |    Resulting Clusters: 0",
            align="left"
        )

        cmds.button(
            label="Create Guides",
            height=32,
            command=self.read_and_create_guides
        )

        cmds.button(
            label="Reverse Direction",
            height=28,
            command=self.reverse_direction
        )


        # -----------------------------------------------------
        # 2. BUILD JOINTS
        # -----------------------------------------------------

        cmds.separator(height=18, style="none")

        cmds.text(
            label="2. BUILD JOINTS",
            align="left",
            font="boldLabelFont"
        )

        cmds.separator(height=3, style="in")

        cmds.button(
            label="Build Joints",
            height=32,
            command=self.build_joints
        )




        # -----------------------------------------------------
        # 3. COLLIDER SETUP
        # -----------------------------------------------------

        cmds.separator(height=9, style="none")

        cmds.text(
            label="3. COLLIDER SETUP",
            align="left",
            font="boldLabelFont"
        )

        cmds.separator(height=3, style="in")


        # -----------------------------------------------------
        # Collider
        # -----------------------------------------------------

        cmds.text(
            label="Collider",
            align="left"
        )

        cmds.rowLayout(
            numberOfColumns=3,
            adjustableColumn=1,
            columnWidth3=(280, 70, 30),
            columnAttach=[
                (1, "both", 0),
                (2, "left", 6),
                (3, "left", 4)
            ]
        )

        self.collider_field = cmds.textField(
            editable=False,
            placeholderText="Select NURBS collider..."
        )

        cmds.button(
            label="Set",
            width=70,
            command=self.set_collider
        )

        cmds.button(
            label="?",
            width=30,
            command=self.show_collider_help
        )

        cmds.setParent("..")


        # -----------------------------------------------------
        # Driver Joints
        # -----------------------------------------------------

        cmds.separator(height=6, style="none")

        cmds.text(
            label="Driver Joints",
            align="left"
        )

        cmds.rowLayout(
            numberOfColumns=2,
            adjustableColumn=1,
            columnWidth2=(320, 70),
            columnAttach=[
                (1, "both", 0),
                (2, "left", 6)
            ]
        )

        self.collider_driver_field = cmds.textField(
            editable=False,
            placeholderText="Select collider driver joints..."
        )

        cmds.button(
            label="Set",
            width=70,
            command=self.set_collider_driver_joints
        )

        cmds.setParent("..")

        # -----------------------------------------------------
        # Skin Source Mesh
        # -----------------------------------------------------

        cmds.separator(height=6, style="none")

        cmds.text(
            label="Skin Source Mesh",
            align="left"
        )

        cmds.rowLayout(
            numberOfColumns=2,
            adjustableColumn=1,
            columnWidth2=(320, 70),
            columnAttach=[
                (1, "both", 0),
                (2, "left", 6)
            ]
        )

        self.collider_skin_source_field = cmds.textField(
            editable=False,
            placeholderText="Select skinned source mesh..."
        )

        cmds.button(
            label="Set",
            width=70,
            command=self.set_collider_skin_source
        )

        cmds.setParent("..")

        # -----------------------------------------------------
        # Prepare Collider
        # -----------------------------------------------------

        cmds.separator(height=3, style="none")

        cmds.button(
            label="Prepare Collider",
            height=32,
            command=self.prepare_collider
        )

                
        # -----------------------------------------------------
        # 4. BUILD KEEPOUT + IK
        # -----------------------------------------------------

        cmds.separator(height=3, style="none")

        cmds.text(
            label="4. BUILD KEEPOUT + IK",
            align="left",
            font="boldLabelFont"
        )

        cmds.separator(height=3, style="in")

        cmds.button(
            label="Build KeepOut + Connect Collider",
            height=32,
            command=self.build_keepout_and_connect
        )

        cmds.button(
            label="Collision Tuning...",
            height=28,
            command=self.open_collision_tuning
        )

        # -----------------------------------------------------
        # 5. MANUAL CONTROLS
        # -----------------------------------------------------

        cmds.separator(height=12, style="none")

        cmds.text(
            label="5. MANUAL CONTROLS",
            align="left",
            font="boldLabelFont"
        )

        cmds.separator(height=3, style="in")

        cmds.rowLayout(
            numberOfColumns=2,
            adjustableColumn=1,
            columnWidth2=(195, 195),
            columnAttach=[
                (1, "both", 0),
                (2, "both", 6)
            ]
        )

        cmds.button(
            label="Select CTRLs",
            height=32,
            command=self.select_manual_ctrls
        )

        cmds.button(
            label="Reset CTRLs",
            height=32,
            command=self.reset_manual_ctrls
        )

        cmds.setParent("..")

        cmds.separator(height=12, style="none")

        cmds.text(
            label="6. SKINNING",
            align="left",
            font="boldLabelFont"
        )

        cmds.separator(height=6, style="none")

        cmds.text(
            label="CTRL Color",
            align="left"
        )

        self.ctrl_color_picker = cmds.colorSliderGrp(
            label="",
            rgb=self.ctrl_colors[
                self.get_section_key()
            ],
            columnWidth3=(10, 60, 200)
        )

        cmds.button(
            label="Apply Color",
            height=28,
            command=self.apply_ctrl_color
        )


        cmds.separator(height=3, style="in")

        
        cmds.button(
            label="Select Weight Joints",
            height=32,
            command=self.select_weight_joints
        )

        cmds.separator(height=3, style="none")

        cmds.setParent("..")  # Close columnLayout
        cmds.setParent("..")  # Close scrollLayout

        cmds.showWindow(self.window)
        
        
    # ---------------------------------------------------------
    # WORLD VERTEX NORMAL
    # ---------------------------------------------------------

    def get_world_vertex_normal(self, vertex):

        # Mesh path + vertex index szétválasztása.
        mesh_transform = vertex.split(".vtx[")[0]

        vertex_id = int(
            vertex.split(".vtx[")[1].split("]")[0]
        )

        # Maya API DAG path.
        selection_list = om.MSelectionList()
        selection_list.add(mesh_transform)

        dag_path = selection_list.getDagPath(0)

        # Ha transformot kaptunk, továbbmegyünk a mesh shape-re.
        if dag_path.apiType() == om.MFn.kTransform:
            dag_path.extendToShape()

        mesh_fn = om.MFnMesh(
            dag_path
        )

        # Explicit WORLD SPACE vertex normal.
        world_normal = mesh_fn.getVertexNormal(
            vertex_id,
            True,
            om.MSpace.kWorld
        )

        world_normal.normalize()

        return world_normal


    # ---------------------------------------------------------
    # BUILD JOINTS
    # ---------------------------------------------------------

    def build_joints(self, *args):



        # -----------------------------------------------------
        # Current section
        # -----------------------------------------------------

        section_key = self.get_section_key()

        section_group = "guides_{}_GRP".format(
            section_key
        )

        if not cmds.objExists(section_group):
            cmds.warning(
                "AutoSkirt: No guides found for section '{}'."
                .format(section_key)
            )
            return


        # -----------------------------------------------------
        # Collect guide locators
        # -----------------------------------------------------

        children = cmds.listRelatives(
            section_group,
            children=True,
            type="transform",
            fullPath=True
        ) or []

        guide_prefix = "guide_{}_".format(
            section_key
        )

        guides = []

        for child in children:

            short_name = child.split("|")[-1]

            if not short_name.startswith(guide_prefix):
                continue
            suffix = short_name.rsplit("_", 1)[-1]

            if not suffix.isdigit():
                continue

            guides.append(child)


        # -----------------------------------------------------
        # Sort guides by number
        # -----------------------------------------------------

        def guide_number(guide):

            short_name = guide.split("|")[-1]

            return int(
                short_name.rsplit("_", 1)[-1]
            )


        guides.sort(
            key=guide_number
        )


        # -----------------------------------------------------
        # Validate
        # -----------------------------------------------------

        if len(guides) < 2:
            cmds.warning(
                "AutoSkirt: At least 2 guides are required."
            )
            return


        # -----------------------------------------------------
        # Print guide order + source vertices
        # -----------------------------------------------------

        print(
            "\n--- AutoSkirt Build Joints Input ---"
        )

        print(
            "Section:",
            section_key
        )

        print(
            "Guide count:",
            len(guides)
        )

        print(
            "Resulting clusters:",
            len(guides) - 1
        )

        print("\nGuide order:")


        for guide in guides:

            if not cmds.attributeQuery(
                "sourceVertex",
                node=guide,
                exists=True
            ):
                cmds.warning(
                    "AutoSkirt: Guide has no sourceVertex: {}"
                    .format(guide)
                )
                return

            source_vertex = cmds.getAttr(
                guide + ".sourceVertex"
            )

            print(
                "{}  ->  {}".format(
                    guide.split("|")[-1],
                    source_vertex
                )
            )


        print(
            "\nAutoSkirt: Guide input validation OK."
        )
        
        # -----------------------------------------------------
        # Existing joint protection
        # -----------------------------------------------------

        existing_start_joint = "skirt_{}_jnt_01".format(
            section_key
        )

        existing_end_joint = "skirt_{}_End_jnt_01".format(
            section_key
        )

        if (
            cmds.objExists(existing_start_joint)
            or cmds.objExists(existing_end_joint)
        ):
            cmds.warning(
                "AutoSkirt: Joint setup already exists "
                "for section '{}'. Delete the existing "
                "section joints before rebuilding."
                .format(section_key)
            )
            return

        # -----------------------------------------------------
        # Build all joint clusters
        # -----------------------------------------------------

        created_clusters = []

        cluster_count = len(guides) - 1


        for cluster_index in range(cluster_count):

            start_guide = guides[cluster_index]
            end_guide = guides[cluster_index + 1]

            start_vertex = cmds.getAttr(
                start_guide + ".sourceVertex"
            )

            end_vertex = cmds.getAttr(
                end_guide + ".sourceVertex"
            )


            # -------------------------------------------------
            # Source vertex world positions
            # -------------------------------------------------

            start_pos_list = cmds.pointPosition(
                start_vertex,
                world=True
            )

            end_pos_list = cmds.pointPosition(
                end_vertex,
                world=True
            )

            start_pos = om.MVector(
                start_pos_list[0],
                start_pos_list[1],
                start_pos_list[2]
            )

            end_pos = om.MVector(
                end_pos_list[0],
                end_pos_list[1],
                end_pos_list[2]
            )


            # -------------------------------------------------
            # Local X = Start -> End
            # -------------------------------------------------

            x_axis = end_pos - start_pos

            if x_axis.length() < 0.000001:
                cmds.warning(
                    "AutoSkirt: Guide points {} and {} "
                    "are too close.".format(
                        cluster_index + 1,
                        cluster_index + 2
                    )
                )
                return

            x_axis.normalize()


            # -------------------------------------------------
            # World-space garment normal
            # -------------------------------------------------

            raw_normal = self.get_world_vertex_normal(
                start_vertex
            )


            # -------------------------------------------------
            # Build orthogonal joint orientation
            #
            # X = chain direction
            # Z = X cross surface normal
            # Y = Z cross X
            # -------------------------------------------------

            z_axis = x_axis ^ raw_normal

            if z_axis.length() < 0.000001:
                cmds.warning(
                    "AutoSkirt: Cannot calculate orientation "
                    "for cluster {:02d}.".format(
                        cluster_index + 1
                    )
                )
                return

            z_axis.normalize()

            y_axis = z_axis ^ x_axis
            y_axis.normalize()


            # -------------------------------------------------
            # Joint names
            # -------------------------------------------------

            joint_number = cluster_index + 1

            start_joint_name = (
                "skirt_{}_jnt_{:02d}".format(
                    section_key,
                    joint_number
                )
            )

            end_joint_name = (
                "skirt_{}_End_jnt_{:02d}".format(
                    section_key,
                    joint_number
                )
            )


            # -------------------------------------------------
            # Create separate 2-joint hierarchy
            # -------------------------------------------------

            cmds.select(clear=True)

            start_joint = cmds.joint(
                name=start_joint_name,
                position=[
                    start_pos.x,
                    start_pos.y,
                    start_pos.z
                ]
            )

            end_joint = cmds.joint(
                name=end_joint_name,
                position=[
                    end_pos.x,
                    end_pos.y,
                    end_pos.z
                ]
            )


            # -------------------------------------------------
            # Orient Start joint
            # -------------------------------------------------

            world_matrix = [
                x_axis.x, x_axis.y, x_axis.z, 0.0,
                y_axis.x, y_axis.y, y_axis.z, 0.0,
                z_axis.x, z_axis.y, z_axis.z, 0.0,
                start_pos.x, start_pos.y, start_pos.z, 1.0
            ]

            cmds.xform(
                start_joint,
                worldSpace=True,
                matrix=world_matrix
            )

            cmds.makeIdentity(
                start_joint,
                apply=True,
                translate=False,
                rotate=True,
                scale=False
            )


            # -------------------------------------------------
            # End joint gets same world orientation
            # -------------------------------------------------

            start_matrix = cmds.xform(
                start_joint,
                query=True,
                worldSpace=True,
                matrix=True
            )

            cmds.xform(
                end_joint,
                worldSpace=True,
                matrix=start_matrix
            )

            cmds.xform(
                end_joint,
                worldSpace=True,
                translation=[
                    end_pos.x,
                    end_pos.y,
                    end_pos.z
                ]
            )

            cmds.makeIdentity(
                end_joint,
                apply=True,
                translate=False,
                rotate=True,
                scale=False
            )


            # -------------------------------------------------
            # Store result
            # -------------------------------------------------

            created_clusters.append(
                (
                    start_joint,
                    end_joint
                )
            )


        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        cmds.select(clear=True)

        print(
            "\nAutoSkirt: Created {} joint clusters for '{}'."
            .format(
                len(created_clusters),
                section_key
            )
        )

        for start_joint, end_joint in created_clusters:

            print(
                "   {} -> {}".format(
                    start_joint,
                    end_joint
                )
            )
            
            
        # -------------------------------------------------
        # Automatically build locators
        # -------------------------------------------------

        self.build_locators()
        
        
        
        # ---------------------------------------------------------
        # BUILD LOCATORS
        # ---------------------------------------------------------

    def build_locators(self, *args):

        # -----------------------------------------------------
        # Current section
        # -----------------------------------------------------

        section_key = self.get_section_key()

        joint_prefix = "skirt_{}_jnt_".format(
            section_key
        )


        # -----------------------------------------------------
        # Find Start joints for current section
        # -----------------------------------------------------

        all_joints = cmds.ls(
            type="joint",
            long=True
        ) or []

        start_joints = []

        for joint in all_joints:

            short_name = joint.split("|")[-1]

            if not short_name.startswith(joint_prefix):
                continue

            suffix = short_name.rsplit("_", 1)[-1]

            if not suffix.isdigit():
                continue

            start_joints.append(joint)


        # -----------------------------------------------------
        # Sort by joint number
        # -----------------------------------------------------

        def joint_number(joint):

            short_name = joint.split("|")[-1]

            return int(
                short_name.rsplit("_", 1)[-1]
            )


        start_joints.sort(
            key=joint_number
        )


        # -----------------------------------------------------
        # Validate
        # -----------------------------------------------------

        if not start_joints:
            cmds.warning(
                "AutoSkirt: No joint clusters found "
                "for section '{}'. Build Joints first."
                .format(section_key)
            )
            return


        # -----------------------------------------------------
        # Print result
        # -----------------------------------------------------

        print(
            "\n--- AutoSkirt Build Locators Input ---"
        )

        print(
            "Section:",
            section_key
        )

        print(
            "Joint cluster count:",
            len(start_joints)
        )

        print("\nStart joints:")

        for joint in start_joints:

            print(
                "   {}".format(
                    joint.split("|")[-1]
                )
            )

        print(
            "\nAutoSkirt: Locator input validation OK."
        )
        
        # -----------------------------------------------------
        # Existing locator protection
        # -----------------------------------------------------

        first_locator = "loc_skirt_{}_{:02d}".format(
            section_key,
            1
        )

        if cmds.objExists(first_locator):
            cmds.warning(
                "AutoSkirt: Locator setup already exists "
                "for section '{}'. Delete the existing "
                "section locators before rebuilding."
                .format(section_key)
            )
            return


        # -----------------------------------------------------
        # Create locators at Start joint positions
        # -----------------------------------------------------

        created_locators = []

        for index, start_joint in enumerate(
            start_joints,
            start=1
        ):

            locator_name = "loc_skirt_{}_{:02d}".format(
                section_key,
                index
            )

            locator = cmds.spaceLocator(
                name=locator_name
            )[0]

            # -------------------------------------------------
            # Match Transform to Start joint
            # Position + Rotation
            # -------------------------------------------------

            cmds.matchTransform(
                locator,
                start_joint,
                position=True,
                rotation=True
            )

            # -------------------------------------------------
            # Freeze Transform
            # -------------------------------------------------

            cmds.makeIdentity(
                locator,
                apply=True,
                translate=True,
                rotate=True,
                scale=True
            )
            
                        # -------------------------------------------------
            # Parent joint cluster under locator
            # Keep current world-space transform
            # -------------------------------------------------

            parented_joint = cmds.parent(
                start_joint,
                locator,
                absolute=True
            )[0]

            # A parenting után a joint long path-ja megváltozott.
            # Frissítjük a listában tárolt path-ot.
            start_joints[index - 1] = cmds.ls(
                parented_joint,
                long=True
            )[0]

            created_locators.append(
                locator
            )

        # -----------------------------------------------------
        # Connect locator chain with pointConstraints
        # -----------------------------------------------------

        for index in range(
            len(created_locators) - 1
        ):

            current_start_joint = start_joints[index]

            # A joint már a locator alatt van,
            # ezért lekérjük a hozzá tartozó End jointot.
            child_joints = cmds.listRelatives(
                current_start_joint,
                children=True,
                type="joint",
                fullPath=True
            ) or []

            if not child_joints:
                cmds.warning(
                    "AutoSkirt: End joint not found under '{}'."
                    .format(
                        current_start_joint
                    )
                )
                return

            current_end_joint = child_joints[0]

            next_locator = created_locators[
                index + 1
            ]

            cmds.pointConstraint(
                current_end_joint,
                next_locator,
                maintainOffset=True
            )


        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        cmds.select(clear=True)

        print(
            "\nAutoSkirt: Created {} locators for '{}'."
            .format(
                len(created_locators),
                section_key
            )
        )

        for locator in created_locators:

            print(
                "   {}".format(
                    locator
                )
            )
    # ---------------------------------------------------------
    # COLLIDER SETUP
    # ---------------------------------------------------------

    def set_collider(self, *args):

        selection = cmds.ls(
            selection=True,
            long=True
        )

        # -----------------------------------------------------
        # Validate selection
        # -----------------------------------------------------

        if len(selection) != 1:
            cmds.warning(
                "AutoSkirt: Select exactly one NURBS "
                "surface collider."
            )
            return

        selected_object = selection[0]

        # -----------------------------------------------------
        # Get transform
        # -----------------------------------------------------

        if cmds.nodeType(selected_object) == "nurbsSurface":

            parents = cmds.listRelatives(
                selected_object,
                parent=True,
                fullPath=True
            ) or []

            if not parents:
                cmds.warning(
                    "AutoSkirt: Could not find collider transform."
                )
                return

            collider_transform = parents[0]

        else:
            collider_transform = selected_object

        # -----------------------------------------------------
        # Validate NURBS surface
        # -----------------------------------------------------

        shapes = cmds.listRelatives(
            collider_transform,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        nurbs_shapes = [
            shape
            for shape in shapes
            if cmds.nodeType(shape) == "nurbsSurface"
        ]

        if not nurbs_shapes:
            cmds.warning(
                "AutoSkirt: Selected object is not "
                "a NURBS surface."
            )
            return

        # -----------------------------------------------------
        # Store collider
        # -----------------------------------------------------

        self.collider = cmds.ls(
            collider_transform,
            long=True
        )[0]

        cmds.textField(
            self.collider_field,
            edit=True,
            text=self.collider.split("|")[-1]
        )

        print(
            "AutoSkirt: Collider set to '{}'.".format(
                self.collider
            )
        )
        
    def show_collider_help(self, *args):

        help_window = "AutoSkirtColliderHelp"

        if cmds.window(
            help_window,
            exists=True
        ):
            cmds.deleteUI(
                help_window,
                window=True
            )

        cmds.window(
            help_window,
            title="AutoSkirt - Collider Help",
            widthHeight=(420, 500),
            sizeable=False
        )

        cmds.columnLayout(
            adjustableColumn=True,
            rowSpacing=8
        )

        cmds.separator(
            height=3,style="none"
        )

        cmds.text(
            label="COLLIDER SETUP",
            font="boldLabelFont",
            align="center"
        )

        cmds.separator(
            height=3,
            style="in"
        )

        cmds.text(
            label=(
                "Create and manually fit a NURBS cylinder "
                "around the leg."
            ),
            align="left",
            wordWrap=True
        )

        cmds.separator(
            height=3,
            style="none"
        )

        cmds.text(
            label=(
                "IMPORTANT:\n\n"
                "• The collider must NOT intersect the leg.\n\n"
                "• Leave a small gap between the leg "
                "and the collider.\n\n"
                "• The collider must remain inside "
                "the garment.\n\n"
                "• Leave a gap between the collider "
                "and the garment as well.\n\n"
                "• Manually adjust the collider shape "
                "to match the character."
            ),
            align="left",
            wordWrap=True
        )

        cmds.separator(
            height=12,
            style="in"
        )

        cmds.text(
            label=(
                "LEG  →  GAP  →  COLLIDER  →  GAP  →  GARMENT"
            ),
            font="boldLabelFont",
            align="center"
        )

        cmds.separator(
            height=12,
            style="none"
        )

        cmds.button(
            label="Close",
            height=30,
            command=lambda *x: cmds.deleteUI(
                help_window,
                window=True
            )
        )

        cmds.showWindow(
            help_window
        )


    def set_collider_driver_joints(self, *args):

        selection = cmds.ls(
            orderedSelection=True,
            long=True
        ) or []

        # -----------------------------------------------------
        # Validate selection
        # -----------------------------------------------------

        if not selection:
            cmds.warning(
                "AutoSkirt: Select one or more collider "
                "driver joints."
            )
            return

        invalid_objects = []

        for obj in selection:

            if cmds.nodeType(obj) != "joint":
                invalid_objects.append(obj)

        if invalid_objects:
            cmds.warning(
                "AutoSkirt: Driver selection contains "
                "non-joint objects."
            )
            return

        # -----------------------------------------------------
        # Store Driver Joints
        # -----------------------------------------------------

        self.collider_driver_joints = selection[:]

        short_names = [
            joint.split("|")[-1]
            for joint in self.collider_driver_joints
        ]

        cmds.textField(
            self.collider_driver_field,
            edit=True,
            text=", ".join(short_names)
        )

        print(
            "AutoSkirt: Collider Driver Joints set:"
        )

        for joint in self.collider_driver_joints:
            print(
                "    {}".format(joint)
            )
        
    def set_collider_skin_source(self, *args):

        selection = cmds.ls(
            selection=True,
            long=True
        ) or []

        # -----------------------------------------------------
        # Validate selection
        # -----------------------------------------------------

        if len(selection) != 1:
            cmds.warning(
                "AutoSkirt: Select exactly one skinned "
                "polygon mesh."
            )
            return

        selected_object = selection[0]

        # -----------------------------------------------------
        # Get transform
        # -----------------------------------------------------

        if cmds.nodeType(selected_object) == "mesh":

            parents = cmds.listRelatives(
                selected_object,
                parent=True,
                fullPath=True
            ) or []

            if not parents:
                cmds.warning(
                    "AutoSkirt: Could not find source "
                    "mesh transform."
                )
                return

            mesh_transform = parents[0]

        else:
            mesh_transform = selected_object

        # -----------------------------------------------------
        # Validate polygon mesh
        # -----------------------------------------------------

        shapes = cmds.listRelatives(
            mesh_transform,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        ) or []

        mesh_shapes = [
            shape
            for shape in shapes
            if cmds.nodeType(shape) == "mesh"
        ]

        if not mesh_shapes:
            cmds.warning(
                "AutoSkirt: Skin Source must be "
                "a polygon mesh."
            )
            return

        # -----------------------------------------------------
        # Find skinCluster
        # -----------------------------------------------------

        history = cmds.listHistory(
            mesh_transform
        ) or []

        skin_clusters = cmds.ls(
            history,
            type="skinCluster"
        ) or []

        if not skin_clusters:
            cmds.warning(
                "AutoSkirt: Selected Skin Source Mesh "
                "has no skinCluster."
            )
            return

        # -----------------------------------------------------
        # Store Skin Source
        # -----------------------------------------------------

        self.collider_skin_source = cmds.ls(
            mesh_transform,
            long=True
        )[0]

        cmds.textField(
            self.collider_skin_source_field,
            edit=True,
            text=self.collider_skin_source.split("|")[-1]
        )

        print(
            "AutoSkirt: Skin Source Mesh set to '{}'."
            .format(
                self.collider_skin_source
            )
        )

        print(
            "AutoSkirt: Source skinCluster = '{}'.".format(
                skin_clusters[0]
            )
        )


    def prepare_collider(self, *args):

        # -----------------------------------------------------
        # Validate required inputs
        # -----------------------------------------------------

        if not self.collider:
            cmds.warning(
                "AutoSkirt: Collider is not set."
            )
            return

        if not cmds.objExists(self.collider):
            cmds.warning(
                "AutoSkirt: Collider no longer exists."
            )
            return

        if not self.collider_driver_joints:
            cmds.warning(
                "AutoSkirt: Collider Driver Joints are not set."
            )
            return

        for joint in self.collider_driver_joints:

            if not cmds.objExists(joint):
                cmds.warning(
                    "AutoSkirt: Driver Joint no longer exists: {}"
                    .format(joint)
                )
                return

        if not self.collider_skin_source:
            cmds.warning(
                "AutoSkirt: Skin Source Mesh is not set."
            )
            return

        if not cmds.objExists(self.collider_skin_source):
            cmds.warning(
                "AutoSkirt: Skin Source Mesh no longer exists."
            )
            return

        # -----------------------------------------------------
        # Prevent duplicate skinCluster
        # -----------------------------------------------------

        collider_history = cmds.listHistory(
            self.collider
        ) or []

        existing_skin_clusters = cmds.ls(
            collider_history,
            type="skinCluster"
        ) or []

        if existing_skin_clusters:
            cmds.warning(
                "AutoSkirt: Collider already has a skinCluster."
            )
            return
            
        # -----------------------------------------------------
        # Bind collider to selected Driver Joints
        # -----------------------------------------------------

        collider_skin = cmds.skinCluster(
            self.collider_driver_joints,
            self.collider,
            toSelectedBones=True,
            bindMethod=0,
            normalizeWeights=1,
            name="autoSkirt_collider_skinCluster"
        )[0]

        print(
            "AutoSkirt: Collider bound successfully."
        )

        print(
            "AutoSkirt: Collider skinCluster = '{}'.".format(
                collider_skin
            )
        )

        # -----------------------------------------------------
        # Copy Skin Weights
        # Source Mesh -> Collider
        # -----------------------------------------------------

        source_history = cmds.listHistory(
            self.collider_skin_source
        ) or []

        source_skin_clusters = cmds.ls(
            source_history,
            type="skinCluster"
        ) or []

        if not source_skin_clusters:
            cmds.warning(
                "AutoSkirt: Could not find source skinCluster."
            )
            return

        source_skin = source_skin_clusters[0]

        cmds.copySkinWeights(
            sourceSkin=source_skin,
            destinationSkin=collider_skin,
            noMirror=True,
            surfaceAssociation="closestPoint",
            influenceAssociation=[
                "name",
                "closestJoint"
            ]
        )

        print(
            "AutoSkirt: Skin weights copied successfully."
        )

        # -----------------------------------------------------
        # Convert collider to Muscle/Bone
        # -----------------------------------------------------

        cmds.select(
            self.collider,
            replace=True
        )

        mel.eval(
            "cMuscle_makeMuscle(0);"
        )

        print(
            "AutoSkirt: Collider converted to Muscle/Bone."
        )
            
    def build_keepout(self, *args):

        section = self.get_section_key()

        locator_pattern = "loc_skirt_{}_??".format(
            section
        )

        locators = cmds.ls(
            locator_pattern,
            type="transform",
            long=True
        ) or []

        locators = sorted(
            locators,
            key=lambda x: int(
                x.rsplit("_", 1)[-1]
            )
        )

        if not locators:
            cmds.warning(
                "AutoSkirt: No locators found for section '{}'.".format(
                    section
                )
            )
            return

        cmds.select(
            locators,
            replace=True
        )

        print(
            "AutoSkirt DEBUG: Calling cMuscle_rigKeepOutSel..."
        )

        result = mel.eval(
            "cMuscle_rigKeepOutSel();"
        )
        
        print(
            "AutoSkirt DEBUG: cMuscle_rigKeepOutSel finished."
        )
        
        # -----------------------------------------------------
        # Restore joint roots directly under locator
        # -----------------------------------------------------

        for locator in locators:

            keepout_driven = cmds.listRelatives(
                locator,
                allDescendents=True,
                type="transform",
                fullPath=True
            ) or []

            keepout_driven = [
                node for node in keepout_driven
                if node.split("|")[-1].endswith("Driven")
            ]

            if not keepout_driven:
                cmds.warning(
                    "AutoSkirt: KeepOutDriven not found under '{}'.".format(
                        locator
                    )
                )
                continue

            keepout_driven = keepout_driven[0]
            
            # -------------------------------------------------
            # Set KeepOut direction
            # -------------------------------------------------

            keepout_shapes = cmds.listRelatives(
                keepout_driven,
                parent=True,
                fullPath=True
            ) or []

            if keepout_shapes:

                keepout_transform = keepout_shapes[0]

                keepout_shape = cmds.listRelatives(
                    keepout_transform,
                    shapes=True,
                    type="cMuscleKeepOut",
                    fullPath=True
                ) or []

                if keepout_shape:

                    keepout_shape = keepout_shape[0]

                    direction_map = {
                        "front_L": (0.0, 0.0, 1.0),
                        "front_R": (0.0, 0.0, 1.0),
                        "side_L": (-1.0, 0.0, 0.0),
                        "side_R": (1.0, 0.0, 0.0),
                        "back_L": (0.0, 0.0, -1.0),
                        "back_R": (0.0, 0.0, -1.0)
                    }

                    direction = direction_map.get(section)

                    if direction:

                        cmds.setAttr(
                            keepout_shape + ".inDirectionX",
                            direction[0]
                        )

                        cmds.setAttr(
                            keepout_shape + ".inDirectionY",
                            direction[1]
                        )

                        cmds.setAttr(
                            keepout_shape + ".inDirectionZ",
                            direction[2]
                        )

            joint_children = cmds.listRelatives(
                keepout_driven,
                children=True,
                type="joint",
                fullPath=True
            ) or []

            if not joint_children:
                cmds.warning(
                    "AutoSkirt: Joint root not found under '{}'.".format(
                        keepout_driven
                    )
                )
                continue

            start_joint = joint_children[0]

            cmds.parent(
                start_joint,
                locator,
                absolute=True
            )

            print(
                "AutoSkirt: Restored joint under locator: {}".format(
                    start_joint.split("|")[-1]
                )
            )
            
            # -------------------------------------------------
            # Restore pointConstraint directly under locator
            # -------------------------------------------------

            point_constraints = cmds.listRelatives(
                keepout_driven,
                children=True,
                type="pointConstraint",
                fullPath=True
            ) or []

            for point_constraint in point_constraints:

                cmds.parent(
                    point_constraint,
                    locator,
                    absolute=True
                )

                print(
                    "AutoSkirt: Restored pointConstraint under locator: {}".format(
                        point_constraint.split("|")[-1]
                    )
                )

            # -------------------------------------------------
            # Create RP IK for joint cluster
            # -------------------------------------------------

            start_joints = cmds.listRelatives(
                locator,
                children=True,
                type="joint",
                fullPath=True
            ) or []

            if not start_joints:
                cmds.warning(
                    "AutoSkirt: Start joint not found under '{}'.".format(
                        locator
                    )
                )
                continue

            start_joint = start_joints[0]

            end_joints = cmds.listRelatives(
                start_joint,
                children=True,
                type="joint",
                fullPath=True
            ) or []

            if not end_joints:
                cmds.warning(
                    "AutoSkirt: End joint not found under '{}'.".format(
                        start_joint
                    )
                )
                continue

            end_joint = end_joints[0]

            locator_short = locator.split("|")[-1]

            ik_name = "ik_{}".format(
                locator_short.replace("loc_", "")
            )

            ik_handle, ik_effector = cmds.ikHandle(
                name=ik_name,
                startJoint=start_joint,
                endEffector=end_joint,
                solver="ikRPsolver"
            )

            manual_group_name = "{}_Manual_GRP".format(
                locator_short.replace("loc_", "")
            )

            manual_group = cmds.group(
                empty=True,
                name=manual_group_name
            )

            cmds.matchTransform(
                manual_group,
                ik_handle,
                position=True,
                rotation=True
            )

            cmds.parent(
                manual_group,
                keepout_driven,
                absolute=True
            )

            cmds.parent(
                ik_handle,
                manual_group,
                absolute=True
            )
            

            
            
            # -------------------------------------------------
            # Create manual CTRL
            # -------------------------------------------------

            ctrl_name = "{}_CTRL".format(
                locator_short.replace("loc_", "")
            )

            # -------------------------------------------------
            # Get garment normal for manual CTRL orientation
            # -------------------------------------------------

            source_vertex = None

            guide_name = "guide_{}_{:02d}".format(
                section,
                int(locator_short.rsplit("_", 1)[-1])
            )

            if cmds.objExists(guide_name + ".sourceVertex"):
                source_vertex = cmds.getAttr(
                    guide_name + ".sourceVertex"
                )

            if source_vertex:
                ctrl_normal = self.get_world_vertex_normal(
                    source_vertex
                )

                print(
                    "AutoSkirt CTRL NORMAL: {} -> "
                    "X={:.4f}, Y={:.4f}, Z={:.4f}".format(
                        locator_short,
                        ctrl_normal.x,
                        ctrl_normal.y,
                        ctrl_normal.z
                    )
                )
            else:
                cmds.warning(
                    "AutoSkirt: Source vertex not found for '{}'.".format(
                        locator_short
                    )
                )




            manual_ctrl = cmds.curve(
                name=ctrl_name,
                degree=1,
                point=[
                    (-3.0,  0.0,  0.0),
                    (-1.8,  0.9,  0.0),
                    (-1.8,  0.3,  0.0),
                    ( 1.8,  0.3,  0.0),
                    ( 1.8,  0.9,  0.0),
                    ( 3.0,  0.0,  0.0),
                    ( 1.8, -0.9,  0.0),
                    ( 1.8, -0.3,  0.0),
                    (-1.8, -0.3,  0.0),
                    (-1.8, -0.9,  0.0),
                    (-3.0,  0.0,  0.0)
                ]
            )
            
            # -------------------------------------------------
            # Set initial CTRL color
            # -------------------------------------------------

            self.set_ctrl_shape_color(
                manual_ctrl,
                self.ctrl_colors[section]
            )            

            # -------------------------------------------------
            # Orient CTRL shape to garment normal
            # -------------------------------------------------
            
            # 90 degree Y correction for arrow shape
            y_correction = om.MEulerRotation(
                0.0,
                om.MAngle(90.0, om.MAngle.kDegrees).asRadians(),
                0.0
            )
            

            source_normal = om.MVector(
                0.0,
                0.0,
                1.0
            )

            target_normal = om.MVector(
                ctrl_normal.x,
                ctrl_normal.y,
                ctrl_normal.z
            )

            target_normal.normalize()

            rotation = source_normal.rotateTo(
                target_normal
            )

            ctrl_cvs = cmds.ls(
                manual_ctrl + ".cv[*]",
                flatten=True
            ) or []

            for cv in ctrl_cvs:

                position = cmds.xform(
                    cv,
                    query=True,
                    objectSpace=True,
                    translation=True
                )

                point = om.MVector(
                    position[0],
                    position[1],
                    position[2]
                )

                point = point.rotateBy(
                    y_correction
                )

                point = point.rotateBy(
                    rotation
                )

                cmds.xform(
                    cv,
                    objectSpace=True,
                    translation=(
                        point.x,
                        point.y,
                        point.z
                    )
                )
                        

            cmds.matchTransform(
                manual_ctrl,
                manual_group,
                position=True,
                rotation=True
            )

            cmds.makeIdentity(
                manual_ctrl,
                apply=True,
                translate=True,
                rotate=True,
                scale=True
            )
            
            # -------------------------------------------------
            # Insert manual CTRL between Manual_GRP and IK
            # -------------------------------------------------

            cmds.parent(
                manual_ctrl,
                manual_group,
                absolute=True
            )

            cmds.makeIdentity(
                manual_ctrl,
                apply=True,
                translate=True,
                rotate=True,
                scale=True
            )

            cmds.parent(
                ik_handle,
                manual_ctrl,
                absolute=True
            )
            
                        # -------------------------------------------------
            # Lock unused manual CTRL channels
            # -------------------------------------------------

            for attr in (
                "rotateX",
                "rotateY",
                "rotateZ",
                "scaleX",
                "scaleY",
                "scaleZ"
            ):
                cmds.setAttr(
                    manual_ctrl + "." + attr,
                    lock=True,
                    keyable=False,
                    channelBox=False
                )


            
            
            
        

            print(
                "AutoSkirt: IK created: {} -> {}".format(
                    start_joint.split("|")[-1],
                    end_joint.split("|")[-1]
                )
            )


        print(
            "AutoSkirt: KeepOut rig created for section '{}':".format(
                section
            )
        )

        # -------------------------------------------------
        # Clean up guides for current section
        # -------------------------------------------------

        section_guide_group = "guides_{}_GRP".format(
            section
        )

        if cmds.objExists(section_guide_group):
            cmds.delete(
                section_guide_group
            )

        # Remove AUTO_SKIRT_GUIDES only when empty.
        guides_root = "AUTO_SKIRT_GUIDES"

        if cmds.objExists(guides_root):

            remaining_children = cmds.listRelatives(
                guides_root,
                children=True
            ) or []

            if not remaining_children:
                cmds.delete(
                    guides_root
                )

        self.guide_vertices = []

        print(
            "AutoSkirt: Guides cleaned up for section '{}'."
            .format(
                section
            )
        )


        
        # -----------------------------------------------------
        # Convert Collider to Muscle/Bone
        # -----------------------------------------------------

        cmds.select(
            self.collider,
            replace=True
        )

        mel.eval(
            "cMuscle_makeMuscle(0);"
        )

        print(
            "AutoSkirt: Collider converted to Muscle/Bone."
        )
        
    def get_collider_muscle_shape(self):

        if not self.collider or not cmds.objExists(self.collider):
            return None

        shapes = cmds.listRelatives(
            self.collider,
            shapes=True,
            fullPath=True
        ) or []

        for shape in shapes:
            if cmds.nodeType(shape) == "cMuscleObject":
                return shape

        return None
        
        
    def get_section_keepout_shapes(self):

        section_key = self.get_section_key()

        locator_pattern = "loc_skirt_{}_??".format(
            section_key
        )

        locators = cmds.ls(
            locator_pattern,
            type="transform",
            long=True
        ) or []

        keepout_shapes = []

        for locator in locators:

            descendants = cmds.listRelatives(
                locator,
                allDescendents=True,
                fullPath=True
            ) or []

            for node in descendants:

                if cmds.nodeType(node) == "cMuscleKeepOut":
                    keepout_shapes.append(node)
                    break

        return keepout_shapes 
    
    def apply_keepout_direction(self, field, *args):

        keepout_shapes = self.get_section_keepout_shapes()

        if not keepout_shapes:
            cmds.warning(
                "No KeepOut nodes found for current section."
            )
            return

        values = cmds.floatFieldGrp(
            field,
            query=True,
            value=True
        )

        for keepout in keepout_shapes:

            if not cmds.objExists(keepout + ".inDirection"):
                continue

            cmds.setAttr(
                keepout + ".inDirection",
                values[0],
                values[1],
                values[2],
                type="double3"
            )

        cmds.refresh(force=True)

        print(
            "AutoSkirt: KeepOut direction applied to {}: "
            "X={:.3f}, Y={:.3f}, Z={:.3f}".format(
                self.get_section_key(),
                values[0],
                values[1],
                values[2]
            )
        )
        
    def flip_keepout_direction(self, field, *args):

        values = list(
            cmds.floatFieldGrp(
                field,
                query=True,
                value=True
            )
        )

        section_key = self.get_section_key()

        if section_key in (
            "side_L",
            "side_R"
        ):
            values[0] *= -1.0

        elif section_key in (
            "front_L",
            "front_R",
            "back_L",
            "back_R"
        ):
            values[2] *= -1.0

        else:
            cmds.warning(
                "Unknown AutoSkirt section."
            )
            return

        cmds.floatFieldGrp(
            field,
            edit=True,
            value1=values[0],
            value2=values[1],
            value3=values[2]
        )

        self.apply_keepout_direction(field)    
            
            
            
        
    def open_collision_tuning(self, *args):
        
        muscle_shape = self.get_collider_muscle_shape()

        if not muscle_shape:
            cmds.warning(
                "Current collider has no cMuscleObject shape. "
                "Run Prepare Collider first."
            )
            return

        sliding_strength = cmds.getAttr(
            muscle_shape + ".slidingStrength"
        )
        fat_value = cmds.getAttr(
            muscle_shape + ".fat"
        )
        
        keepout_shapes = self.get_section_keepout_shapes()

        if not keepout_shapes:
            cmds.warning(
                "No KeepOut nodes found for current section."
            )
            return

        direction = cmds.getAttr(
            keepout_shapes[0] + ".inDirection"
        )[0]
        
        
        window_name = "autoSkirtCollisionTuning"

        if cmds.window(
            window_name,
            exists=True
        ):
            cmds.deleteUI(window_name)

        window = cmds.window(
            window_name,
            title="AutoSkirt - Collision Tuning",
            sizeable=False,
            widthHeight=(320, 280)
        )

        cmds.columnLayout(
            adjustableColumn=True,
            rowSpacing=8
        )

        cmds.separator(height=8, style="none")

        cmds.text(
            label="COLLISION TUNING",
            align="center",
            font="boldLabelFont"
        )

        cmds.separator(height=8, style="in")

        cmds.text(
            label="Collider Settings",
            align="left"
        )

        cmds.floatSliderGrp(
            label="Sliding Strength",
            field=True,
            minValue=0.0,
            maxValue=10.0,
            fieldMinValue=0.0,
            fieldMaxValue=100.0,
            value=sliding_strength,
            columnWidth3=(110, 60, 120),
            dragCommand=lambda value: cmds.setAttr(
                muscle_shape + ".slidingStrength",
                value
            ),
            changeCommand=lambda value: cmds.setAttr(
                muscle_shape + ".slidingStrength",
                value
            )
        )

        cmds.floatSliderGrp(
            label="Fat",
            field=True,
            minValue=0.0,
            maxValue=10.0,
            fieldMinValue=0.0,
            fieldMaxValue=100.0,
            value=fat_value,
            columnWidth3=(110, 60, 120),
            dragCommand=lambda value: cmds.setAttr(
                muscle_shape + ".fat",
                value
            ),
            changeCommand=lambda value: cmds.setAttr(
                muscle_shape + ".fat",
                value
            )
        )

        cmds.separator(height=8, style="in")

        cmds.text(
            label="KeepOut Direction",
            align="left"
        )

        direction_field = cmds.floatFieldGrp(
            numberOfFields=3,
            label="X / Y / Z",
            value1=direction[0],
            value2=direction[1],
            value3=direction[2],
            columnWidth4=(110, 60, 60, 60)
        )

        cmds.floatFieldGrp(
            direction_field,
            edit=True,
            changeCommand=lambda *_: self.apply_keepout_direction(
                direction_field
            )
        )

        cmds.button(
            label="Flip Main Direction",
            command=lambda *_: self.flip_keepout_direction(
                direction_field
            )
        )

        cmds.separator(height=5, style="none")

        cmds.button(
            label="Close",
            command=lambda *_: cmds.deleteUI(window_name)
        )

        cmds.separator(height=8, style="none")

        cmds.showWindow(window)    
    
     # ---------------------------------------------------------
    # BUILD KEEPOUT + CONNECT COLLIDER
    # ---------------------------------------------------------

    def build_keepout_and_connect(self, *args):

        section = self.get_section_key()

        # Validate prepared Muscle collider
        muscle_shape = self.get_collider_muscle_shape()

        if not muscle_shape:
            cmds.warning(
                "AutoSkirt: Prepare Collider first."
            )
            return

        locator_pattern = "loc_skirt_{}_??".format(
            section
        )

        locators = cmds.ls(
            locator_pattern,
            type="transform",
            long=True
        ) or []

        if not locators:
            cmds.warning(
                "AutoSkirt: No locators found for section '{}'.".format(
                    section
                )
            )
            return

        # Build existing KeepOut + IK system
        self.build_keepout()

        # Verify every locator has KeepOut and CTRL
        for locator in locators:

            locator_short = locator.split("|")[-1]

            ctrl_name = "{}_CTRL".format(
                locator_short.replace("loc_", "")
            )

            keepout_shapes = cmds.listRelatives(
                locator,
                allDescendents=True,
                type="cMuscleKeepOut",
                fullPath=True
            ) or []

            if not keepout_shapes or not cmds.objExists(ctrl_name):
                cmds.warning(
                    "AutoSkirt: Incomplete KeepOut rig at '{}'.".format(
                        locator_short
                    )
                )
                return

        # Connect collider using existing function
        self.connect_collider_to_keepout()

        print(
            "AutoSkirt: Build + Connect completed for '{}'.".format(
                section
            )
        )   
    
        
    def connect_collider_to_keepout(self, *args):

        # -----------------------------------------------------
        # Validate collider
        # -----------------------------------------------------

        if not self.collider:
            cmds.warning(
                "AutoSkirt: Collider is not set."
            )
            return

        if not cmds.objExists(self.collider):
            cmds.warning(
                "AutoSkirt: Collider no longer exists."
            )
            return

        # -----------------------------------------------------
        # Find current section locators
        # -----------------------------------------------------

        section = self.get_section_key()

        locator_pattern = "loc_skirt_{}_??".format(
            section
        )

        locators = cmds.ls(
            locator_pattern,
            type="transform",
            long=True
        ) or []

        locators = sorted(
            locators,
            key=lambda x: int(
                x.rsplit("_", 1)[-1]
            )
        )

        if not locators:
            cmds.warning(
                "AutoSkirt: No locators found for section '{}'.".format(
                    section
                )
            )
            return

        # -----------------------------------------------------
        # Select locators + collider
        # Maya wrapper resolves KeepOut and Muscle shapes
        # -----------------------------------------------------

        cmds.select(
            locators,
            replace=True
        )

        cmds.select(
            self.collider,
            add=True
        )

        # -----------------------------------------------------
        # Connect Muscle collider to KeepOuts
        # -----------------------------------------------------

        mel.eval(
            "cMuscle_keepOutAddRemMuscle(1);"
        )
        
        
        # -------------------------------------------------
        # Organize AutoSkirt root locators
        # -------------------------------------------------

        rig_group = "AUTO_SKIRT_RIG_GRP"

        if not cmds.objExists(rig_group):
            rig_group = cmds.group(
                empty=True,
                name=rig_group
            )

        locators = cmds.ls(
            "loc_skirt_*",
            type="transform",
            long=True
        ) or []

        root_locators = []

        for locator in locators:

            parent = cmds.listRelatives(
                locator,
                parent=True,
                fullPath=True
            )

            if not parent:
                root_locators.append(
                    locator
                )

        if root_locators:
            cmds.parent(
                root_locators,
                rig_group,
                absolute=True
            )

        print(
            "AutoSkirt: {} root locators organized under {}.".format(
                len(root_locators),
                rig_group
            )
        )        
        
        
        

        print(
            "AutoSkirt: Collider connected to KeepOuts for section '{}'.".format(
                section
            )
        )        

    # ---------------------------------------------------------
    # GARMENT MESH
    # ---------------------------------------------------------

    def set_garment_mesh(self, *args):

        selection = cmds.ls(
            selection=True,
            objectsOnly=True,
            long=True
        )

        if not selection:
            cmds.warning("AutoSkirt: Select a garment mesh first.")
            return

        obj = selection[0]

        # Ha transform van kijelölve, megkeressük a mesh shape-et.
        if cmds.nodeType(obj) == "transform":

            shapes = cmds.listRelatives(
                obj,
                shapes=True,
                noIntermediate=True,
                fullPath=True
            ) or []

            mesh_shapes = [
                shape for shape in shapes
                if cmds.nodeType(shape) == "mesh"
            ]

            if not mesh_shapes:
                cmds.warning(
                    "AutoSkirt: Selected object is not a polygon mesh."
                )
                return

        elif cmds.nodeType(obj) != "mesh":

            cmds.warning(
                "AutoSkirt: Selected object is not a polygon mesh."
            )
            return

        # Shape esetén a transformot tároljuk.
        if cmds.nodeType(obj) == "mesh":

            parent = cmds.listRelatives(
                obj,
                parent=True,
                fullPath=True
            )

            if not parent:
                cmds.warning(
                    "AutoSkirt: Could not find mesh transform."
                )
                return

            obj = parent[0]

        self.garment_mesh = obj

        cmds.textField(
            self.mesh_field,
            edit=True,
            text=obj.split("|")[-1]
        )

       

        print("AutoSkirt Garment Mesh:", self.garment_mesh)
        
    # ---------------------------------------------------------
    # SELECT WEIGHT JOINTS
    # ---------------------------------------------------------

    def select_weight_joints(self, *args):

        joints = cmds.ls(
            "skirt_*",
            type="joint",
            long=True
        ) or []

        weight_joints = [
            joint for joint in joints
            if "_End_jnt_" not in joint.split("|")[-1]
        ]

        if not weight_joints:
            cmds.warning(
                "AutoSkirt: No weight joints found."
            )
            return

        cmds.select(
            weight_joints,
            replace=True
        )

        print(
            "AutoSkirt: {} weight joints selected.".format(
                len(weight_joints)
            )
        )

    # ---------------------------------------------------------
    # SELECT MANUAL CONTROLS
    # ---------------------------------------------------------

    def select_manual_ctrls(self, *args):

        section = self.get_section_key()

        ctrl_pattern = "skirt_{}_*_CTRL".format(
            section
        )

        controls = cmds.ls(
            ctrl_pattern,
            type="transform",
            long=True
        ) or []

        if not controls:
            cmds.warning(
                "AutoSkirt: No Manual CTRLs found for '{}'.".format(
                    section
                )
            )
            return

        cmds.select(
            controls,
            replace=True
        )

        print(
            "AutoSkirt: {} Manual CTRLs selected for '{}'.".format(
                len(controls),
                section
            )
        )


    # ---------------------------------------------------------
    # RESET MANUAL CONTROLS
    # ---------------------------------------------------------

    def reset_manual_ctrls(self, *args):

        section = self.get_section_key()

        ctrl_pattern = "skirt_{}_*_CTRL".format(
            section
        )

        controls = cmds.ls(
            ctrl_pattern,
            type="transform",
            long=True
        ) or []

        if not controls:
            cmds.warning(
                "AutoSkirt: No Manual CTRLs found for '{}'.".format(
                    section
                )
            )
            return

        for ctrl in controls:

            for attr in (
                "translateX",
                "translateY",
                "translateZ"
            ):

                plug = ctrl + "." + attr

                if cmds.getAttr(plug, lock=True):
                    continue

                if cmds.listConnections(
                    plug,
                    source=True,
                    destination=False
                ):
                    continue

                cmds.setAttr(
                    plug,
                    0.0
                )

        print(
            "AutoSkirt: Manual CTRLs reset for '{}'.".format(
                section
            )
        )

    # ---------------------------------------------------------
    # APPLY COLOR TO CTRL SHAPES
    # ---------------------------------------------------------

    def set_ctrl_shape_color(self, ctrl, color):

        shapes = cmds.listRelatives(
            ctrl,
            shapes=True,
            fullPath=True
        ) or []

        for shape in shapes:

            if cmds.nodeType(shape) != "nurbsCurve":
                continue

            cmds.setAttr(
                shape + ".overrideEnabled",
                1
            )

            cmds.setAttr(
                shape + ".overrideRGBColors",
                1
            )

            cmds.setAttr(
                shape + ".overrideColorRGB",
                color[0],
                color[1],
                color[2],
                type="double3"
            )


    # ---------------------------------------------------------
    # UPDATE CTRL COLOR PICKER
    # ---------------------------------------------------------

    def update_ctrl_color_picker(self, *args):

        section = self.get_section_key()

        color = self.ctrl_colors[section]

        cmds.colorSliderGrp(
            self.ctrl_color_picker,
            edit=True,
            rgb=color
        )


    # ---------------------------------------------------------
    # APPLY COLOR TO CURRENT SECTION
    # ---------------------------------------------------------

    def apply_ctrl_color(self, *args):

        section = self.get_section_key()

        color = cmds.colorSliderGrp(
            self.ctrl_color_picker,
            query=True,
            rgb=True
        )

        self.ctrl_colors[section] = tuple(color)

        ctrl_pattern = "skirt_{}_*_CTRL".format(
            section
        )

        controls = cmds.ls(
            ctrl_pattern,
            type="transform",
            long=True
        ) or []

        for ctrl in controls:
            self.set_ctrl_shape_color(
                ctrl,
                color
            )

        print(
            "AutoSkirt: Color applied to {} CTRLs in '{}'.".format(
                len(controls),
                section
            )
        )


    # ---------------------------------------------------------
    # SECTION
    # ---------------------------------------------------------

    def get_section_key(self):

        section = cmds.optionMenu(
            self.section_menu,
            query=True,
            value=True
        )

        section_map = {
            "Front Left": "front_L",
            "Front Right": "front_R",
            "Left Side": "side_L",
            "Right Side": "side_R",
            "Back Left": "back_L",
            "Back Right": "back_R"
        }

        return section_map[section]

    # ---------------------------------------------------------
    # VERTEX SELECTION
    # ---------------------------------------------------------

    def read_vertex_selection(self, *args):

        if not self.garment_mesh:
            cmds.warning(
                "AutoSkirt: Set a garment mesh first."
            )
            return

        # Ordered selection.
        selection = cmds.ls(
            orderedSelection=True,
            flatten=True,
            long=True
        ) or []

        if not selection:
            cmds.warning(
                "AutoSkirt: Select at least 2 vertices."
            )
            return

        # -----------------------------------------------------
        # Csak vertex componenteket fogadunk el.
        # -----------------------------------------------------

        invalid_components = [
            item for item in selection
            if ".vtx[" not in item
        ]

        if invalid_components:
            cmds.warning(
                "AutoSkirt: Selection must contain vertices only."
            )
            return

        # -----------------------------------------------------
        # Ellenőrizzük, hogy minden vertex a garment meshhez
        # tartozik-e.
        # -----------------------------------------------------

        garment_long = cmds.ls(
            self.garment_mesh,
            long=True
        )[0]

        valid_vertices = []

        for vertex in selection:

            vertex_object = vertex.split(".vtx[")[0]

            vertex_object_long = cmds.ls(
                vertex_object,
                long=True
            )

            if not vertex_object_long:
                cmds.warning(
                    "AutoSkirt: Could not resolve vertex object."
                )
                return

            vertex_object_long = vertex_object_long[0]

            if vertex_object_long != garment_long:
                cmds.warning(
                    "AutoSkirt: All vertices must belong to the "
                    "selected Garment Mesh."
                )
                return

            valid_vertices.append(vertex)

        # -----------------------------------------------------
        # Minimum két guide point szükséges.
        # -----------------------------------------------------

        guide_count = len(valid_vertices)

        if guide_count < 2:
            cmds.warning(
                "AutoSkirt: Select at least 2 consecutive vertices."
            )
            return

        cluster_count = guide_count - 1

        # Most már biztonságosan eltárolhatjuk.
        self.guide_vertices = valid_vertices[:]

        # -----------------------------------------------------
        # UI update
        # -----------------------------------------------------

        cmds.text(
            self.selection_info,
            edit=True,
            label=(
                "Selected Guide Points: {}    |    "
                "Resulting Clusters: {}"
            ).format(
                guide_count,
                cluster_count
            )
        )

        section = cmds.optionMenu(
            self.section_menu,
            query=True,
            value=True
        )

       

        print("\nAutoSkirt Ordered Vertices:")

        for index, vertex in enumerate(
            valid_vertices,
            start=1
        ):
            print(
                "{:02d}: {}".format(index, vertex)
            )
        return True
        
    def read_and_create_guides(self, *args):

        success = self.read_vertex_selection()

        if not success:
            return

        self.create_guides()

    # ---------------------------------------------------------
    # CREATE GUIDES
    # ---------------------------------------------------------

    def create_guides(self, *args):

        if not self.garment_mesh:
            cmds.warning(
                "AutoSkirt: Set a garment mesh first."
            )
            return

        if len(self.guide_vertices) < 2:
            cmds.warning(
                "AutoSkirt: Read a valid vertex selection first."
            )
            return

        section_key = self.get_section_key()

        # -----------------------------------------------------
        # Master guide group
        # -----------------------------------------------------

        master_group = "AUTO_SKIRT_GUIDES"

        if not cmds.objExists(master_group):
            master_group = cmds.group(
                empty=True,
                name=master_group
            )

        # -----------------------------------------------------
        # Section group
        # -----------------------------------------------------

        section_group = "guides_{}_GRP".format(
            section_key
        )

        # Egyelőre nem írunk felül létező sectiont.
        if cmds.objExists(section_group):
            cmds.warning(
                "AutoSkirt: Guides already exist for "
                "section '{}'.".format(section_key)
            )
            return

        section_group = cmds.group(
            empty=True,
            name=section_group,
            parent=master_group
        )

        created_guides = []

        # -----------------------------------------------------
        # Locatorok létrehozása
        # -----------------------------------------------------

        for index, vertex in enumerate(
            self.guide_vertices,
            start=1
        ):

            position = cmds.pointPosition(
                vertex,
                world=True
            )

            guide_name = "guide_{}_{:02d}".format(
                section_key,
                index
            )

            locator = cmds.spaceLocator(
                name=guide_name
            )[0]

            cmds.xform(
                locator,
                worldSpace=True,
                translation=position
            )

            cmds.parent(
                locator,
                section_group
            )
            # -------------------------------------------------
            # Source vertex tárolása a guide-on
            # -------------------------------------------------

            cmds.addAttr(
                locator,
                longName="sourceVertex",
                dataType="string"
            )

            cmds.setAttr(
                locator + ".sourceVertex",
                vertex,
                type="string"
            )
            
            # -------------------------------------------------
            # Guide transformok lockolása
            # -------------------------------------------------

            for attribute in [
                "translateX", "translateY", "translateZ",
                "rotateX", "rotateY", "rotateZ",
                "scaleX", "scaleY", "scaleZ"
            ]:
                cmds.setAttr(
                    locator + "." + attribute,
                    lock=True,
                    keyable=False,
                    channelBox=False
                )

            created_guides.append(locator)            
            
        # -----------------------------------------------------
        # Guide preview curve
        # -----------------------------------------------------

        guide_positions = []

        for guide in created_guides:

            position = cmds.xform(
                guide,
                query=True,
                worldSpace=True,
                translation=True
            )

            guide_positions.append(position)

        preview_curve = cmds.curve(
            degree=1,
            point=guide_positions,
            name="guide_{}_preview_CRV".format(section_key)
        )

        cmds.parent(
            preview_curve,
            section_group
        )
        
        
        # -----------------------------------------------------
        # Preview curve követi a guide locatorokat
        # -----------------------------------------------------

        preview_shape = cmds.listRelatives(
            preview_curve,
            shapes=True,
            noIntermediate=True,
            fullPath=True
        )[0]

        for index, guide in enumerate(created_guides):

            decompose_node = cmds.createNode(
                "decomposeMatrix",
                name="guide_{}_{:02d}_preview_DM".format(
                    section_key,
                    index + 1
                )
            )

            cmds.connectAttr(
                guide + ".worldMatrix[0]",
                decompose_node + ".inputMatrix",
                force=True
            )

            cmds.connectAttr(
                decompose_node + ".outputTranslate",
                "{}.controlPoints[{}]".format(
                    preview_shape,
                    index
                ),
                force=True
            )



        # -----------------------------------------------------
        # Selection / status
        # -----------------------------------------------------

        cmds.select(
            created_guides,
            replace=True
        )

        

        print(
            "\nAutoSkirt: Created {} guides for '{}'.".format(
                len(created_guides),
                section_key
            )
        )

        for guide in created_guides:
            print("  ", guide)

    # ---------------------------------------------------------
    # REVERSE DIRECTION
    # ---------------------------------------------------------

    def reverse_direction(self, *args):

        section_key = self.get_section_key()

        section_group = "guides_{}_GRP".format(
            section_key
        )

        if not cmds.objExists(section_group):
            cmds.warning(
                "AutoSkirt: No guides exist for section '{}'."
                .format(section_key)
            )
            return

        # -----------------------------------------------------
        # Megkeressük a guide locatorokat.
        # -----------------------------------------------------

        children = cmds.listRelatives(
            section_group,
            children=True,
            type="transform",
            fullPath=False
        ) or []

        guide_prefix = "guide_{}_".format(
            section_key
        )

        guides = []

        for child in children:

            # A preview curve-ot nem akarjuk guide-nak tekinteni.
            if (
                child.startswith(guide_prefix)
                and not child.endswith("_preview_CRV")
            ):
                guides.append(child)

        if len(guides) < 2:
            cmds.warning(
                "AutoSkirt: At least 2 guides are required "
                "to reverse direction."
            )
            return

        # -----------------------------------------------------
        # Jelenlegi számozás szerint sorba rendezzük.
        # -----------------------------------------------------

        guides.sort()

        # Megfordítjuk a tényleges sorrendet.
        reversed_guides = list(reversed(guides))

        # -----------------------------------------------------
        # Ideiglenes átnevezés.
        #
        # Erre azért van szükség, mert például:
        #
        # guide_front_01 -> guide_front_05
        #
        # név már létezik.
        # -----------------------------------------------------

        temp_guides = []

        for index, guide in enumerate(
            reversed_guides,
            start=1
        ):

            temp_name = cmds.rename(
                guide,
                "AUTOSKIRT_TEMP_{:02d}".format(index)
            )

            temp_guides.append(temp_name)

        # -----------------------------------------------------
        # Új számozás.
        # -----------------------------------------------------

        renamed_guides = []

        for index, guide in enumerate(
            temp_guides,
            start=1
        ):

            new_name = "guide_{}_{:02d}".format(
                section_key,
                index
            )

            new_name = cmds.rename(
                guide,
                new_name
            )

            renamed_guides.append(new_name)


        # -----------------------------------------------------
        # Status
        # -----------------------------------------------------

        cmds.select(
            renamed_guides,
            replace=True
        )

       

        print(
            "\nAutoSkirt: '{}' direction reversed."
            .format(section_key)
        )

# -------------------------------------------------------------
# RUN
# -------------------------------------------------------------

auto_skirt_ui = AutoSkirtUI()