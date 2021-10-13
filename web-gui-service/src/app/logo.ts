import { isBase64EncodedPng, isNonEmptyString } from "./validations";

export class Logo {

  static throwError(functionName: string, message: string): void {
    let errMsg = `${Logo.name} -- ${functionName}() -- ${message}`;
    throw Error(errMsg);
  }
  
  static withAllAttributes(altText: string, imgSrc: string): Logo {
    let result = new Logo();
    try {
      result.setAltText(altText);
      result.setImgSrc(imgSrc);
    } catch (err) {
      let errMsg = `Failed.\n${err}`;
      Logo.throwError("withAllAttributes", errMsg);
    }
    return result;
  }

  public altText: string;
  public imgSrc: string;

  constructor() {
    this.altText = "Value should have been updated";
    this.imgSrc = "Value should have been updated";
  }

  public setAltText(val: string): void {
    if (this.isAltTextLegal(val)) {
      this.altText = val;
    }
    else {
      Logo.throwError("setAltText", "Expected a non empty string.");
    }
  }

  public setImgSrc(val: string): void {
    if (this.isImgSrcLegal(val)) {
      this.imgSrc = val;
    }
    else {
      Logo.throwError("setImgSrc", "Expected an encoded PNG.");
    }
  }

  private isAltTextLegal(val: string): boolean {
    return isNonEmptyString(val);
  }

  private isImgSrcLegal(val: string): boolean {
    return isBase64EncodedPng(val);
  }

}
