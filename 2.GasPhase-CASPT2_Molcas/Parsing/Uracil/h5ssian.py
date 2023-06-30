import h5py

# Open the .h5 file
filename = "no_ura.slapaf.h5"
with h5py.File(filename, "r") as f:
    # Iterate over all the datasets in the file
    for dataset_name in f:
        # Check if the item is a dataset
        if isinstance(f[dataset_name], h5py.Dataset):
            # Get the data from the dataset
            data = f[dataset_name][()]

            # Create a text file with the same name as the dataset
            output_filename = "{}.txt".format(dataset_name)
            with open(output_filename, "w") as txt_file:
                # Write the data to the text file
                txt_file.write(str(data))

            #print(f"Data from {dataset_name} saved in {output_filename}")
