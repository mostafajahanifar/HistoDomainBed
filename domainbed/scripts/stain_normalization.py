import os
import cv2
import logging
from tqdm import tqdm
from tiatoolbox.tools.stainnorm import MacenkoNormalizer
from multiprocessing import Pool, Manager
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_images(root_dir):
    logging.info(f"Searching for images in {root_dir}...")
    image_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp')):
                image_paths.append(os.path.join(dirpath, filename))
    logging.info(f"Found {len(image_paths)} images.")
    return image_paths

def create_target_dir_structure(source_root, target_root, source_path):
    relative_path = os.path.relpath(source_path, source_root)
    target_path = os.path.join(target_root, relative_path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    return target_path

def process_image(args):
    source_img_path, target_img_path, fitted_normalizer = args
    try:
        source_img = cv2.imread(source_img_path)[..., ::-1]
        normalized_img = fitted_normalizer.transform(source_img)
        cv2.imwrite(target_img_path, normalized_img[..., ::-1])
        # logging.info(f"Processed {source_img_path} and saved to {target_img_path}")
    except Exception as e:
        logging.error(f"Error processing {source_img_path}: {e}")

def normalize_images(source_root, target_root, target_img_path):
    logging.info(f"Reading target image for fitting normalizer: {target_img_path}")
    target_img = cv2.imread(target_img_path)[..., ::-1]

    stain_normalizer = MacenkoNormalizer()
    logging.info("Fitting the stain normalizer with the target image.")
    stain_normalizer.fit(target_img)

    with Manager() as manager:
        shared_normalizer = manager.Namespace()
        shared_normalizer.normalizer = stain_normalizer

        image_paths = find_images(source_root)

        tasks = []
        for source_img_path in image_paths:
            target_img_path = create_target_dir_structure(source_root, target_root, source_img_path)
            tasks.append((source_img_path, target_img_path, shared_normalizer.normalizer))

        logging.info("Starting the normalization process...")
        with Pool(4) as pool:
            progress_bar = tqdm(total=len(tasks), desc=source_root.split("/")[-1])

            def update(*a):
                progress_bar.update()

            for task in tasks:
                pool.apply_async(process_image, args=(task,), callback=update)

            pool.close()
            pool.join()
            progress_bar.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize histology images' stains.")
    parser.add_argument('dataset', type=str, help="The name of the dataset to be processed.")
    args = parser.parse_args()

    dataset = args.dataset
    source_root = f"/home/u2070124/lsf_workspace/Data/Data/domain_generalization/datasets/{dataset}"
    target_root = f"/home/u2070124/lsf_workspace/Data/Data/domain_generalization/datasets_stain_normalized/{dataset}"
    target_img_path = "/home/u2070124/lsf_workspace/Data/Data/domain_generalization/target_stain.png"

    normalize_images(source_root, target_root, target_img_path)