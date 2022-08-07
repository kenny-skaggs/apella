function sortedObjects(objects, propertyName) {
    return Array.from(objects).sort((a, b) => {
        const aValue = a[propertyName];
        const bValue = b[propertyName];
        if (aValue < bValue) {
            return -1;
        } else if (aValue > bValue) {
            return 1;
        } else {
            return 0;
        }
    });
}

function removeObject(objectList, objectToRemove, idProperty) {
    const index = objectList.findIndex((object) => object[idProperty] === objectToRemove[idProperty]);
    if (index >= 0) {
        objectList.splice(index, 1);
    }
}

function removeById(objectList, idProperty, id) {
    const index = objectList.findIndex((object) => object[idProperty] === id);
    if (index >= 0) {
        objectList.splice(index, 1);
    }
}

export default {
    sortedObjects,
    removeObject,
    removeById
};
