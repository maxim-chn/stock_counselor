function isBase64EncodedPng(val: string): boolean {
  if (isNonEmptyString(val)) {
    let regexp = new RegExp("^data:image/png;base64,");
    return regexp.test(val);
  }
  return false;
}

function isInteger(val: Number): boolean {
  if (val) {
    return val > 0;
  }
  return false;
}

function isLink(val: string): boolean {
  if (isNonEmptyString(val)) {
    let regexp = new RegExp("^(http|https):\\/\\/[www]*[a-z,.,\\/]*$")
    return regexp.test(val);
  }
  return false;
}

function isNonEmptyString(val: string): boolean {
  if (val) {
    return val.length > 0;
  }
  return false;
}

export {
  isBase64EncodedPng,
  isInteger,
  isLink,
  isNonEmptyString
}