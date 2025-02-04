import streamlit as st
import numpy as np
import trimesh
import os
import tempfile
from pathlib import Path
import zipfile
import io

st.set_page_config(
    page_title="STL File Splitter",
    page_icon="🔨",
    layout="wide"
)

def calculate_splits(model_size, max_size):
    if max_size is None or max_size <= 0:
        raise ValueError("Maximum size must be a positive number.")
    splits = np.ceil(model_size / max_size)
    return int(splits)

def create_zip_file(files):
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in files:
            file_name = os.path.basename(file_path)
            zip_file.write(file_path, file_name)
    return zip_io.getvalue()

def split_stl_into_grid(input_stl, xsplit=None, ysplit=None, max_x=None, max_y=None, flip=False):
    # Load the STL file
    mesh = trimesh.load(input_stl)
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("Failed to load STL as a valid 3D mesh")

    # Flip the mesh if specified
    if flip:
        rotation_matrix = trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
        mesh.apply_transform(rotation_matrix)

    # Get the bounding box dimensions
    bounds = mesh.bounds
    model_size_x = bounds[1][0] - bounds[0][0]
    model_size_y = bounds[1][1] - bounds[0][1]
    model_size_z = bounds[1][2] - bounds[0][2]

    # Determine the number of splits using the appropriate method
    if xsplit is None and max_x is not None:
        xsplit = calculate_splits(model_size_x, max_x)
    if ysplit is None and max_y is not None:
        ysplit = calculate_splits(model_size_y, max_y)

    # Ensure at least one split in each direction
    xsplit = max(1, xsplit or 1)
    ysplit = max(1, ysplit or 1)

    # Calculate subdivision sizes
    segment_size_x = model_size_x / xsplit
    segment_size_y = model_size_y / ysplit

    # Create a temporary directory for the output files
    temp_dir = tempfile.mkdtemp()
    output_prefix = Path(input_stl).stem

    # Calculate extents
    x_extent = np.linspace(bounds[0][0], bounds[1][0], xsplit + 1)
    y_extent = np.linspace(bounds[0][1], bounds[1][1], ysplit + 1)
    z_min, z_max = bounds[0][2], bounds[1][2]

    # Split the mesh into grid cells
    output_files = []
    part_number = 1
    for i in range(xsplit):
        for j in range(ysplit):
            x_min, x_max = x_extent[i], x_extent[i + 1]
            y_min, y_max = y_extent[j], y_extent[j + 1]
            bounds_box = trimesh.creation.box(
                extents=(x_max - x_min, y_max - y_min, z_max - z_min),
                transform=trimesh.transformations.translation_matrix(
                    [(x_max + x_min) / 2, (y_max + y_min) / 2, (z_max + z_min) / 2]
                )
            )

            section = mesh.intersection(bounds_box)
            if section.is_empty:
                continue

            output_filename = os.path.join(temp_dir, f"{output_prefix}_splt-{part_number:02d}.stl")
            section.export(output_filename)
            output_files.append(output_filename)
            part_number += 1

    return {
        "dimensions": {
            "x": model_size_x,
            "y": model_size_y,
            "z": model_size_z
        },
        "splits": {
            "x": xsplit,
            "y": ysplit
        },
        "segment_size": {
            "x": segment_size_x,
            "y": segment_size_y,
            "z": model_size_z
        },
        "output_files": output_files
    }

# Streamlit UI
st.title("🔨 STL File Splitter")
st.write("Upload an STL file and split it into smaller parts for 3D printing")

# File uploader
uploaded_file = st.file_uploader("Choose an STL file", type=['stl'])

if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.stl')
    temp_input.write(uploaded_file.getvalue())
    temp_input.close()

    # Radio button to select the splitting method
    split_method = st.radio("Select splitting method", ("Divisions", "Chunk Size"))
    
    if split_method == "Divisions":
        st.subheader("Split by Number of Divisions")
        xsplit = st.number_input("Number of X divisions", min_value=1, value=1)
        ysplit = st.number_input("Number of Y divisions", min_value=1, value=1)
        max_x = None
        max_y = None
    else:  # Chunk Size method
        st.subheader("Split by Chunk Size")
        max_x = st.number_input("Chunk Size in X (mm)", min_value=1.0, value=200.0)
        max_y = st.number_input("Chunk Size in Y (mm)", min_value=1.0, value=200.0)
        xsplit = None
        ysplit = None

    flip = st.checkbox("Flip model over X-axis")

    if st.button("Split STL"):
        with st.spinner("Processing STL file..."):
            try:
                result = split_stl_into_grid(
                    temp_input.name,
                    xsplit=xsplit,
                    ysplit=ysplit,
                    max_x=max_x,
                    max_y=max_y,
                    flip=flip
                )

                # Display results
                st.success("STL file split successfully!")

                # Show dimensions
                st.subheader("Model Dimensions")
                dim_col1, dim_col2, dim_col3 = st.columns(3)
                with dim_col1:
                    st.metric("X Dimension", f"{result['dimensions']['x']:.2f} mm")
                with dim_col2:
                    st.metric("Y Dimension", f"{result['dimensions']['y']:.2f} mm")
                with dim_col3:
                    st.metric("Z Dimension", f"{result['dimensions']['z']:.2f} mm")

                # Show segment information
                st.subheader("Segment Information")
                seg_col1, seg_col2 = st.columns(2)
                with seg_col1:
                    st.write(f"Number of X splits: {result['splits']['x']}")
                    st.write(f"Number of Y splits: {result['splits']['y']}")
                with seg_col2:
                    st.write(f"Segment X size: {result['segment_size']['x']:.2f} mm")
                    st.write(f"Segment Y size: {result['segment_size']['y']:.2f} mm")

                # Create download section
                st.subheader("Download Files")
                
                # Create zip file of all splits
                zip_data = create_zip_file(result['output_files'])
                original_filename = Path(uploaded_file.name).stem
                st.download_button(
                    label="📦 Download All Splits as ZIP",
                    data=zip_data,
                    file_name=f"{original_filename}_splits.zip",
                    mime="application/zip",
                    help="Download all split files in a single ZIP archive"
                )

                # Individual file downloads (collapsible)
                with st.expander("Individual File Downloads"):
                    for file_path in result['output_files']:
                        with open(file_path, 'rb') as f:
                            file_name = os.path.basename(file_path)
                            st.download_button(
                                label=f"Download {file_name}",
                                data=f,
                                file_name=file_name,
                                mime='application/octet-stream'
                            )

            except Exception as e:
                st.error(f"Error processing STL file: {str(e)}")

            finally:
                # Cleanup temporary files
                os.unlink(temp_input.name)
                for file in result.get('output_files', []):
                    try:
                        os.unlink(file)
                    except Exception:
                        pass

else:
    st.info("Please upload an STL file to begin")

st.markdown("---")
st.markdown("""
### How to use:
1. Upload your STL file using the file uploader above.
2. Select your splitting method:
   - **Divisions**: Specify how many pieces to split the model into.
   - **Chunk Size**: Specify the maximum size for each piece.
3. Optionally flip the model over the X-axis.
4. Click **Split STL** to process the file.
5. Download all splits as a ZIP file or individual pieces.
""")
