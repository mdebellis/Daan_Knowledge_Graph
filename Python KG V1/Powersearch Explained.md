Powersearch Explained
I have made what I think are sufficient comments to understand the powersearch, but I will do a greater explanation here.

Visualizing the Window
The first section of the powersearch is generally pyqt objects. Think of it like this: we have many rows of entry where the user
will select what characteristics they want. Those rows follow the format of "title": "characteristic" which is shown as a either a QformLayout(two column layout) or a QHBoxLayout(row style layout). We then have to gather all these rows so we put them in a QVBoxLayout(vertical layout style). We also have special cases where we needed scrollables and the code for that is quite confusing, I heavily refernced others on stackoverflow and other sites. Hopefully this gives some general insight on how all the widgets and buttons are constructed and organized. Generally, many data parameters --> each gets a row or some other formatting --> all those are sorted vertically.

The SDG Tree
This was very convuluted when I made it. I remember having logic issue with seperating the tree class out of the document, this may be possible and I was simply shortsighted, but now that I'm months removed I'm unsure. What needs to be understood here is the clicked sdgs must be returned to the window class so we call a function in the window class to take in our clicked sdgs. Then we have the issue of what the clicked sdgs actually are. These clicked sdgs only contain labels, so I have an irimapper that can map the labels to the iris. That way they can be used in the query.

Changing the Window
All those intial arrays exist for storing the qt objects are so they can be deleted. When deleting, I literally must pass the object to be deleted in to a deleteLater function, otherwise it doesn't leave the window.

NGO Display
I hope this isn't too complicated, it just pops a new screen for a given ngo.