function removeFromStringArray(collection: Array<string>, val: string): void {
  collection.forEach((element, index) => {
    if (element == val) {
      collection.splice(index, 1);
    }
  });
}

export {
  removeFromStringArray
}