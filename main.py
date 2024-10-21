from PIL import Image, ImageDraw
import numpy as np

def compare_and_mark_images(image_path1, image_path2, output_path):
    # Open the images
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    # Convert images to RGB (in case they are in a different format)
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')

    # Check if images are the same size
    if img1.size != img2.size:
        print("Images are not the same size.")
        return

    # Convert images to numpy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Create a new image for marking differences with the same size as img2
    overlay = Image.new('RGBA', img2.size, (255, 255, 0, 0))  # Yellow color with full transparency
    draw_overlay = ImageDraw.Draw(overlay)

    # Initialize a list to hold differences
    differences = []

    # Compare pixel by pixel
    for y in range(arr1.shape[0]):
        for x in range(arr1.shape[1]):
            if not np.array_equal(arr1[y, x], arr2[y, x]):
                differences.append({
                    'position': (x, y),
                    'color_image1': arr1[y, x].tolist(),
                    'color_image2': arr2[y, x].tolist()
                })
                # Mark the difference on the overlay with yellow color and 50% opacity
                draw_overlay.rectangle([x, y, x + 1, y + 1], fill=(255, 255, 0, 128))  # Yellow with 50% opacity

    # Combine the overlay with the original image
    img2_with_overlay = Image.alpha_composite(img2.convert('RGBA'), overlay)

    # Save the marked image
    img2_with_overlay.save(output_path)

    # Output results
    if differences:
        print(f"Found {len(differences)} differences. Marked in the output image.")
    else:
        print("The images are identical.")

# Example usage
compare_and_mark_images('./img1.jpg', './img3.jpg', 'output.png')