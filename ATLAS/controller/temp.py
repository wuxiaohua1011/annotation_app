class AtlasAnnotationAppWindow(QDialog):
    def __init__(
        self,
        app: QApplication,
        segmentation_file_path: Path = DEFAULT_SEGMENTATION_FILE_PATH,
        style_sheet_path: Path = DEFAULT_STYLE_SHEET_PATH,
        scene_file_path: Path = DEFAULT_SCENE_FILE_PATH,
        show: bool = True,
    ):
        super().__init__()
        self.app = app
        try:
            self.app.setStyleSheet(open(style_sheet_path.as_posix()).read())
        except FileNotFoundError:
            print("Cannot location file {}".format(style_sheet_path.as_posix()))
            pass
        self.ui = Ui_annotation_app()
        self.ui.setupUi(self)

        self.segmentation_file_path = segmentation_file_path
        self.messages = ["Program Started, UI Loaded"]  # list of strings
        self.segments: List[Segment] = []  # list of Segment objects
        self.current_cropped_data: List = []
        self.upperScene = Scene()
        self.lowerScene = Scene()
        self.currentSystemMode = -1
        self.system_mode_clicked()

        self.populateSegmentList()

        ## DEMO
        self.upperScene.render_mesh(fname=scene_file_path)

        self.setupCanvas()
        self.setListener()
        if show:
            self.show()

    """
    Initializer functions
    """

    def setListener(self):
        self.ui.btn_floodfill_done.clicked.connect(self.btn_floodfill_done_clicked)
        self.ui.btn_floodfill_cancel.clicked.connect(self.btn_floodfill_cancel_clicked)
        self.ui.common_load_btn.clicked.connect(self.btn_common_load_clicked)
        self.ui.common_save_btn.clicked.connect(self.btn_save_clicked)
        self.ui.segment_list.itemDoubleClicked.connect(
            self.segmentation_list_item_double_clicked
        )

        self.ui.btn_boundingbox_crop.clicked.connect(self.btn_boundingbox_cropped)
        self.ui.system_mode.currentChanged.connect(self.system_mode_clicked)
        self.ui.btn_boundingbox_translation_xVal.valueChanged.connect(
            self.bbox_update_translate
        )
        self.ui.btn_boundingbox_translation_yVal.valueChanged.connect(
            self.bbox_update_translate
        )
        self.ui.btn_boundingbox_translation_zVal.valueChanged.connect(
            self.bbox_update_translate
        )
        self.ui.btn_boundingbox_translation_reset.clicked.connect(
            self.bbox_reset_translate
        )
        self.ui.btn_boundingbox_rotation_xVal.valueChanged.connect(
            self.bbox_update_rot_x
        )
        self.ui.btn_boundingbox_rotation_yVal.valueChanged.connect(
            self.bbox_update_rot_y
        )
        self.ui.btn_boundingbox_rotation_zVal.valueChanged.connect(
            self.bbox_update_rot_z
        )
        self.ui.btn_boundingbox_rotation_reset.clicked.connect(self.bbox_reset_rotation)
        self.ui.btn_boundingbox_scaling_xVal.valueChanged.connect(
            self.bbox_update_scale
        )
        self.ui.btn_boundingbox_scaling_yVal.valueChanged.connect(
            self.bbox_update_scale
        )
        self.ui.btn_boundingbox_scaling_zVal.valueChanged.connect(
            self.bbox_update_scale
        )
        self.ui.btn_boundingbox_scaling_reset.clicked.connect(self.bbox_reset_scaling)

    def system_mode_clicked(self):
        try:
            # self.currentSystemMode = system_modes.get(self.ui.system_mode.currentIndex(), "UNKNOWN MODE")
            self.currentSystemMode = system_modes[self.ui.system_mode.currentIndex()]
        except KeyError as err:
            self.writeMessage("Cannot understand current system mode")
            print(err)
            exit(1)
        if self.currentSystemMode == "UNKNOWN":
            print("ERR, system mode = -1 ")
        elif self.currentSystemMode == "boundingbox":
            self.start_bbox()
        else:
            pass
            # self.destroy_bbox()

    def setupCanvas(self):
        self.ui.data_display_window.addWidget(self.upperScene.native)
        self.ui.data_display_window.addWidget(self.lowerScene.native)

    """
    Event Listener
    """

    def btn_floodfill_done_clicked(self):
        if len(self.upperScene.selected_point_ids) == 1:
            print("One points detected, floodfilling")
            pcd = mesh_to_pointcloud(self.upperScene.mesh)
            surface_to_crop = floodfill(self.upperScene.selected_point_ids, pcd)
            self.current_cropped_data = surface_to_crop
            new_pcd = crop_reserve(self.upperScene.pcd, surface_to_crop)
            self.lowerScene.render_pcd(new_pcd)
        elif len(self.upperScene.selected_point_ids) == 2:
            self.writeMessage(
                "Two Points <{}> selected so far, instruction is unclear, abort".format(
                    self.upperScene.selected_point_ids
                )
            )
        elif len(self.upperScene.selected_point_ids) == 3:
            print("three points detected, floodfilling")
            pcd = mesh_to_pointcloud(self.upperScene.mesh)
            surface_to_crop = floodfill(self.upperScene.selected_point_ids, pcd)
            self.current_cropped_data = surface_to_crop
            new_pcd = crop_reserve(pcd, surface_to_crop)
            self.lowerScene.render_pcd(new_pcd)
        else:
            self.writeMessage(
                "More than 3 points chosen, not implemented this functionality yet"
            )

    def btn_floodfill_cancel_clicked(self):
        self.upperScene.render_mesh(autoclear=True)
        self.current_cropped_data = []

    def btn_common_load_clicked(self):
        filename = openFileNamesDialog(self)
        # do filetype checking here
        if filename:
            import os

            dirpath = os.getcwd()
            relative_path = filename.replace(dirpath, ".")
            # self.current_data_file_name = relative_path  # TODO this might cause issue later on
            self.writeMessage("Opening file <{}>".format(filename))

            self.upperScene.render_mesh(filename)
            self.current_cropped_data = []

    def btn_save_clicked(self):
        response = prompt_saving()

        if response.get("seg_name", "") == "":
            self.writeMessage("Please provide a segmentation name")
        else:
            # assume that the state of the program should have existing segments all read in from file
            # from initializing the program.
            if (
                len(self.upperScene.selected_point_ids) == 0
                and self.currentSystemMode == 0
            ):
                self.writeMessage("There are no points to save")
            else:
                new_seg = Segment(
                    id=len(self.segments),
                    data_file_name=self.upperScene.pcd_fname,
                    segment_name=response.get("seg_name"),
                    indices=self.current_cropped_data,
                    type_class=(response.get("type_class", "Unknown Class"), 1),
                )
                self.segments.append(new_seg)
                self.ui.segment_list.addItem(
                    "{} | {} | {}".format(
                        new_seg.id, new_seg.segment_name, new_seg.type_class
                    )
                )

                self.writeSegments()
                # can we just remove the bbox and floodfill markings instead and leave the rest
                if self.currentSystemMode == 0:
                    self.lowerScene.clear()
                    self.upperScene.selected_point_ids = []
                    self.upperScene.render_mesh(autoclear=True)
                self.writeMessage("Data Saved")
                self.current_cropped_data = []

    def segmentation_list_item_double_clicked(self):
        current_item_text = self.ui.segment_list.currentItem().text()
        try:
            current_item_index = int(current_item_text.split(" | ")[0])
            selected_segment = self.segments[current_item_index]

            self.upperScene.render_mesh(
                fname=Path(selected_segment.data_file_name),
                indices_to_highlight=selected_segment.indices,
                autoclear=True,
            )
            # color = np.asarray(pcd.colors)
            # for i in index_to_highlight:
            #     color[i] = (0, 1, 0)
            # pcd.colors = o3d.utility.Vector3dVector(color)
            # self.current_result_point_indices.extend(index_to_highlight)
            # self.upperScene.pcd_render(pcd)

        except ValueError as e:
            self.writeMessage(
                "ERR: Index is not an int --> {}".format(
                    current_item_text.split(" | ")[0]
                )
            )

    """
    Helper functions
    """

    def writeMessage(self, message):
        self.messages.append(message)
        self.ui.message_center_text_edit.append("> {}\n".format(message))

    def populateSegmentList(self):
        self.segments.clear()
        self.ui.segment_list.clear()
        try:
            new_segs = readSegmentation(self.segmentation_file_path)
            for new_seg in new_segs:
                self.segments.append(new_seg)
                self.ui.segment_list.addItem(
                    "{} | {} | {}".format(
                        new_seg.id, new_seg.segment_name, new_seg.type_class
                    )
                )
        except FileNotFoundError:
            self.writeMessage("No segments read")

    def writeSegments(self):
        with open(self.segmentation_file_path, mode="w") as f:
            json.dump(
                [json.loads(segment.json()) for segment in self.segments], f, indent=4
            )

    def start_bbox(self):
        self.children_before_bbox = len(self.upperScene.view.children[0].children)

        try:
            self.bbox
        except:
            self.bbox = BBOX()
        self.bbox_outlines = [
            Line(
                pos=np.array(outline),
                color="r",
                width=5,
                connect="strip",
                method="gl",
                antialias=True,
            )
            for outline in self.bbox.get_outline()
        ]
        # self.view.add adds a reference
        [self.upperScene.view.add(outline) for outline in self.bbox_outlines]

    def destroy_bbox(self):
        for child in self.upperScene.view.children[0].children:
            if type(child) != vispy.scene.visuals.Mesh:
                child.parent = None

    def vis_bbox(self):
        new_outline = self.bbox.get_outline()
        for i in range(len(new_outline)):
            convert_array = np.array(
                [ind_array.tolist() for ind_array in new_outline[i]]
            )
            self.bbox_outlines[i].set_data(convert_array)
            self.bbox_outlines[i].update_markers(convert_array)

    def bbox_update_translate(self):
        self.bbox.set_translate(
            self.ui.btn_boundingbox_translation_xVal.value(),
            self.ui.btn_boundingbox_translation_yVal.value(),
            self.ui.btn_boundingbox_translation_zVal.value(),
        )
        self.vis_bbox()

    def bbox_update_rot_x(self):
        self.bbox.set_x_rot(self.ui.btn_boundingbox_rotation_xVal.value())
        self.vis_bbox()

    def bbox_update_rot_y(self):
        self.bbox.set_y_rot(self.ui.btn_boundingbox_rotation_yVal.value())
        self.vis_bbox()

    def bbox_update_rot_z(self):
        self.bbox.set_z_rot(self.ui.btn_boundingbox_rotation_zVal.value())
        self.vis_bbox()

    def bbox_update_scale(self):
        self.bbox.set_scale(
            self.ui.btn_boundingbox_scaling_xVal.value(),
            self.ui.btn_boundingbox_scaling_yVal.value(),
            self.ui.btn_boundingbox_scaling_zVal.value(),
        )
        self.vis_bbox()

    def bbox_reset_translate(self):
        self.ui.btn_boundingbox_translation_xVal.setValue(0)
        self.ui.btn_boundingbox_translation_yVal.setValue(0)
        self.ui.btn_boundingbox_translation_zVal.setValue(0)

    def bbox_reset_rotation(self):
        self.ui.btn_boundingbox_rotation_xVal.setValue(0)
        self.ui.btn_boundingbox_rotation_yVal.setValue(0)
        self.ui.btn_boundingbox_rotation_zVal.setValue(0)

    def bbox_reset_scaling(self):
        self.ui.btn_boundingbox_scaling_xVal.setValue(1)
        self.ui.btn_boundingbox_scaling_yVal.setValue(1)
        self.ui.btn_boundingbox_scaling_zVal.setValue(1)

    def btn_boundingbox_cropped(self):
        try:
            tmp_pointcloud = o3d.geometry.PointCloud()
            tmp_pointcloud.points = self.upperScene.mesh.vertices
            tmp_pointcloud.colors = self.upperScene.mesh.vertex_colors
            bb_to_crop = self.bbox.crop_idx(tmp_pointcloud)
            new_pcd = crop_reserve(tmp_pointcloud, bb_to_crop[0].tolist())
            self.lowerScene.render_pcd(new_pcd)
            self.current_cropped_data = bb_to_crop[0].tolist()
        except Exception as e:
            print("error")
            print(e)
            self.writeMessage(str(e))
        self.writeMessage("Selected Points is cleared")


class Scene(scene.SceneCanvas):
    def __init__(self):
        scene.SceneCanvas.__init__(self, keys="interactive", size=(800, 800))
        self.unfreeze()
        self.camera_mode = "turntable"
        self.pcd = None
        self.marker = None
        self.view = self.central_widget.add_view()
        self.view.camera = self.camera_mode
        self.selected_point_ids = []
        self.point_size = 3.5
        self.additional_elements = []
        self.mesh: o3d.geometry.TriangleMesh = None
        self.pcd_fname = None

    def render_mesh(self, fname: Path = None, autoclear=False, indices_to_highlight=[]):
        if autoclear:
            self.clear()
        mesh = None
        if fname is None:
            mesh = copy.deepcopy(self.mesh)
        else:
            mesh = o3d.io.read_triangle_mesh(fname.as_posix())
            self.mesh = mesh
            self.pcd_fname = fname.as_posix()
            self.pcd = mesh_to_pointcloud(mesh)
        if len(indices_to_highlight) != 0:
            color = np.asarray(mesh.vertex_colors)
            for i in indices_to_highlight:
                color[i] = (0, 1, 0)
            mesh.vertex_colors = o3d.utility.Vector3dVector(color)
        self.render_helper(mesh)

    def render_helper(self, mesh):
        points = np.asarray(mesh.vertices)
        faces = np.asarray(
            mesh.triangles
        )  # nx3 array of ints each element is the index of point in the triangle

        # create scatter object and fill in the data
        scatter = scene.visuals.Mesh(
            vertices=points, faces=faces, vertex_colors=mesh.vertex_colors
        )
        self.view.add(scatter)

    def render_pcd(self, pcd, autoclear_view=True):
        if autoclear_view:
            self.clear()
        points = np.asarray(pcd.points)
        colors = np.asarray(pcd.colors)
        self.marker = scene.visuals.Markers()
        self.marker.set_gl_state("translucent", blend=True, depth_test=True)
        self.marker.set_data(
            points, edge_color=colors, face_color=colors, size=self.point_size
        )
        self.view.add(self.marker)

    def clear(self):
        self.central_widget.remove_widget(self.view)
        self.view = self.central_widget.add_view()
        self.additional_elements = []
        self.selected_point_ids = []
        self.view.camera = self.camera_mode

    def onMouseRelease(self, event):
        if event.button == 1 and distance_traveled(event.trail()) <= 2:
            try:
                selected_point_coord = self.findClickingCoord(event)
                if len(selected_point_coord) > 0:
                    selected_point_id = self.findPointIDFromClick(
                        selected_point_coord, 1
                    )[
                        0
                    ]  # select only one point at a time
                    self.selected_point_ids.append(selected_point_id)
                if len(self.selected_point_ids) == 2:
                    points = np.asarray(self.mesh.vertices)
                    pt1 = points[self.selected_point_ids[0]]
                    pt2 = points[self.selected_point_ids[1]]
                    self.draw_line(pt1, pt2)
            except Exception as e:
                print(e)
                pass

    def findPointIDFromClick(self, coord, n):
        """
        :param coord: centering coordinate
        :param n: number of closest point to coord
        :return: return n closest point to coord
        """
        pcd_tree = o3d.geometry.KDTreeFlann(self.mesh)
        [k, idx, _] = pcd_tree.search_knn_vector_3d(coord, n)
        return [idx.pop() for i in range(n)]

    def findClickingCoord(self, event):
        points = np.asarray(self.mesh.vertices)
        # colors = np.asarray(pcd.colors)
        # axis = scene.visuals.XYZAxis(parent=self.upper.scene)

        # prepare list of unique colors needed for picking
        ids = np.arange(1, len(points) + 1, dtype=np.uint32).view(np.uint8)
        ids = ids.reshape(-1, 4)
        ids = np.divide(ids, 255, dtype=np.float32)
        screen_pos = self.view.scene.transform.map(points)
        screen_pos = screen_pos[:, 0:2]

        # tmp = screen_pos - event.pos
        # all in marker coordinates
        # create point on line of clicked point but offset by in z direction
        # create direction of line as difference between clicked point and offset point
        # unit normalize direction
        # project candidate points to line
        # pick best candidate based on distance on line
        clicked_point = self.view.scene.transform.imap(event.pos)
        offset_point = np.asarray([event.pos[0], event.pos[1], 0.000001, 1])
        offset_point = self.view.scene.transform.imap(offset_point)
        direction = clicked_point - offset_point
        direction = direction[0:3]
        direction = direction / np.linalg.norm(direction)

        diff = np.linalg.norm(screen_pos - event.pos, axis=1)
        # print("min of diff =", min(diff))
        good_idxs = np.where(diff <= min(diff))[0]  # @Dapo
        # good_idxs = np.where(diff < 2)[0]
        candidate_points = points[good_idxs]
        centered_points = candidate_points - clicked_point[0:3]
        distances = np.matmul(centered_points, direction.reshape((3, 1)))
        good_idx = np.argmax(distances)

        tmp_point = candidate_points[good_idx, 0:3]
        tmp_point = tmp_point[
            np.newaxis, :
        ]  # reshape it to fit it into marker.set_data

        marker = scene.visuals.Markers()
        marker.set_gl_state("opaque", blend=False, depth_test=False)
        marker.set_data(tmp_point, edge_color="red", face_color="red", size=5.0)
        self.view.add(marker)

        return tmp_point[0]  # since we are only selecting 1 point at a time

    def draw_line(self, pt1, pt2):
        line = vispy.scene.visuals.Line(
            pos=np.asarray([pt1, pt2]),
            color="red",
            width=10,
            connect="strip",
            method="gl",
            antialias=False,
        )
        line.set_gl_state("opaque", blend=False, depth_test=False)
        self.view.add(line)
