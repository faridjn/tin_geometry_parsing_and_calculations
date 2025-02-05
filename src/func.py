def parse_tin_geometry(xml_file):
    """
    Parses a TIN geometry from an XML file and returns:
    - points (dict): A dictionary mapping point IDs to NumPy coordinate arrays.
    - faces (list): A list of triangular faces, represented as point index triplets.
    """
    points = {}  # Dictionary to store point ID -> coordinates
    faces = []   # List to store triangular faces

    # Read the XML file
    try:
        with open(xml_file, 'r', encoding='utf-8') as file:
            xml_soup = bs(file, 'lxml-xml')
    except Exception as e:
        raise ValueError(f"Error reading XML file: {e}")

    # Extract faces (F) and convert them to lists of integer indices
    for face in xml_soup.find_all('F'):
        face_list = [int(x) for x in face.text.split()]
        if len(face_list) == 3:  # Ensure valid triangular face
            faces.append(face_list)

    # Extract points (P) and store them in the dictionary
    for point_tag in xml_soup.find_all('P'):
        try:
            pid = int(point_tag["id"])
            point_list = [float(x) for x in point_tag.text.split()]
            if len(point_list) == 3:  # Ensure 3D coordinates
                points[pid] = np.array(point_list)
        except (KeyError, ValueError) as e:
            raise ValueError(f"Invalid point entry: {point_tag}. Error: {e}")

    return points, faces


def compute_triangle_area(v1, v2, v3):
    """
    Computes the area of a triangle in 3D space using the cross-product method.
    The area is 1/2 * cross product of two edge vectors.
    """
    v1, v2, v3 = map(np.asarray, (v1, v2, v3))     
    return 0.5 * np.linalg.norm(np.cross(v2 - v1, v3 - v1))


def compute_weighted_centroid(points, faces):
    """ 
    Computes the area-weighted centroid of a Triangulated Irregular Network (TIN).
    
    Args:
        points (dict): Mapping of point IDs to NumPy 3D coordinate arrays.
        faces (list): List of triangular faces (each containing three point IDs).
    
    Returns:
        np.ndarray: 3D coordinates of the area-weighted centroid, or None if invalid.
    """
    total_weighted_centroid = np.zeros(3)
    total_area = 0

    for face in faces:
        try:
            v1, v2, v3 = points[face[0]], points[face[1]], points[face[2]]
        except KeyError:
            raise ValueError(f"Face references non-existent point IDs: {face}")

        area = compute_triangle_area(v1, v2, v3)
        centroid = (v1 + v2 + v3) / 3.0

        total_weighted_centroid += area * centroid
        total_area += area

    return total_weighted_centroid / total_area if total_area > 0 else None
