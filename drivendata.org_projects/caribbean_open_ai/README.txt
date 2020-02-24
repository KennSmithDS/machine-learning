Open AI Caribbean Challenge: Mapping Disaster Risk from Aerial Imagery

Jupyter Notebook Descriptions:

1) caribbean_image_trainer.ipynb - primary notebook used in building file paths for each country, importing and parsing aerial image files based on geojson coordinates, performing image scaling and manipulation, and tested using a few CNN frameworks (e.g. CNN, VGG16).
2) file_splitter.ipynb - split images into test and train paths after the image trainer parsed the raw .tif into smaller images based on rooftop material category
3) simple_classivier.ipynb - cleaner implementation of using VGG16 model to determine accuracy of predictive model

Problem description:
In this challenge, you will be predicting roof type from drone imagery. The data consists of a set of overhead imagery of seven locations across three countries with labeled building footprints. Your goal is to classify each of the building footprints with the roof material type.

The only features in this dataset are the images themselves and the building footprints in the GeoJSONs. The images consist of seven large high-resolution Cloud Optimized GeoTiffs of the seven different areas. The spatial resolution of the images is roughly 4 cm.

Labels:
Each image1 corresponds to train and test GeoJSONs, where labels are encoded as FeatureCollections. metadata.csv links the each image with its corresponding GeoJSON. For each area in the train set, the GeoJSON includes the unique building ID, building footprint, roof material, and verified field (see note above). For each area in the test set, the GeoJSON contains just the unique building ID and building footprint.

Roof material labels are also provided in train_labels.csv, where each row contains a unique building ID followed by five roof material columns, with a 1.0 indicating that building's roof type and 0.0s in the remaining columns. Each building has only one roof type.

Data format:
A STAC (SpatioTemporal Asset Catalog)2 of the imagery and label data is provided. The STAC is organized with a root catalog, containing sub-catalogs for each country. Each country contains collections for the various areas within that country.

An area collection links to STAC items — one for the imagery, one for the training label data, and if that region has test building footprints, an item for those labels. The imagery STAC item geometry is the footprint of the image. The training data label items have overviews that give the class counts for each of the roof_material classes contained in the labeled data.

Performance metric:
To measure your model's accuracy by looking at prediction error, we'll use a metric called log loss. This is an error metric, so a lower value is better (as opposed to an accuracy metric, where a higher value is better). Log loss can be calculated as follows:

loss = −(1/N) * ∑i=1N ∑j=1M [yij*log*pij]
where N is the number of observations, M is the number of classes (in terms of our problem M=5), yij is a binary variable indicating if classification for observation i was correct, and pij was the user-predicted probability that label j applies to observation i.

In Python you can easily calculate log loss using the scikit-learn function sklearn.metrics.log_loss. R users may find the MultiLogLoss function in the MLmetrics package.

Project Website: 
https://www.drivendata.org/competitions/58/disaster-response-roof-type/

Data Source: 
https://s3.amazonaws.com/drivendata-public-assets/stac.tar

