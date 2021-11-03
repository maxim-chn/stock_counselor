function addToStringArrayIfNotPresent(collection: Array<string>, val: string): void {
  let necessaryElements = Array<string>();
  let valIsPresent = false;
  
  for (let element = collection.pop(); element != undefined; element = collection.pop()) {
    
    if (element == val) {
      valIsPresent = true;
    }
    
    necessaryElements.push(element);
  }
  
  for (let element = necessaryElements.pop(); element != undefined; element = necessaryElements.pop()) {
    collection.push(element);
  }

  if (!valIsPresent) {
    collection.push(val);
  }
}

function removeFromStringArray(collection: Array<string>, val: string): void {
  let necessaryElements = Array<string>();
  
  for (let element = collection.pop(); element != undefined; element = collection.pop()) {
    
    if (element != val) {
      necessaryElements.push(element);
    }
  }
  
  for (let element = necessaryElements.pop(); element != undefined; element = necessaryElements.pop()) {
    collection.push(element);
  }
}

export {
  addToStringArrayIfNotPresent,
  removeFromStringArray
}