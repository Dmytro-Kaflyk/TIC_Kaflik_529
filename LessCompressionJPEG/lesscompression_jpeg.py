def run_jpeg_tests():
    images = ["image1.jpg", "image2.jpg", "image3.jpg"]
    quant_tables = ["quant_table_1", "quant_table_2"]

    for img_name in images:
        for quant_table in quant_tables:
            filepath = f"Results/{img_name}_{quant_table}.bin"
            dc, ac, tables, blocks_count = read_image_file(filepath)


            decoded_img_filename = decoder(dc, ac, tables, blocks_count, quant_table, img_name)

            size_original = os.path.getsize(img_name)
            size_decoded = os.path.getsize(decoded_img_filename)
            ratio = size_original / size_decoded

            with open("results_jpeg.txt", "a") as f:
                f.write(f"Image: {img_name}, Quant table: {quant_table}\n")
                f.write(f"Decoded file size: {size_decoded} bytes\n")
                f.write(f"Original size: {size_original} bytes\n")
                f.write(f"Compression ratio: {ratio:.2f}\n\n")
