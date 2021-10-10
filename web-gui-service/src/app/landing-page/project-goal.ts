import { isBase64EncodedPng, isNonEmptyString } from "../validations";

export class ProjectGoal {

  static withAllAttributes(altText: string, imgSrc: string, text: string) {
    let result = new ProjectGoal();
    try {
      result.setAltText(altText);
      result.setImgSrc(imgSrc);
      result.setText(text);
    } catch (err) {
      let errMsg = `Failed.\n${err}`;
      ProjectGoal.throwError("withAllAttributes", errMsg);
    }
    return result;
  }

  static throwError(functionName: string, message: string): void {
    let errMsg = `${ProjectGoal.name} -- ${functionName}() -- ${message}`;
    throw Error(errMsg);
  }
  
  public altText: string;
  public imgSrc: string;
  public text: string;
  
  constructor() {
    this.altText = "Value should have been updated";
    this.imgSrc = "Value should have been updated";
    this.text = "Value should have been updated";
  }

  public setAltText(val: string): void {
    if (this.isAltTextLegal(val)) {
      this.altText = val;
    }
    else {
      ProjectGoal.throwError("setAltText", "received illegal argument");
    }
  }

  public setImgSrc(val: string): void {
    if (this.isImgSrcLegal(val)) {
      this.imgSrc = val;
    }
    else {
      ProjectGoal.throwError("setImgSrc", "received illegal argument");
    }
  }

  public setText(val: string): void {
    if (this.isTextLegal(val)) {
      this.text = val;
    }
    else {
      ProjectGoal.throwError("setText", "received illegal argument");
    }
  }

  private isAltTextLegal(val: string): boolean {
    return isNonEmptyString(val);

  }

  private isImgSrcLegal(val: string): boolean {
    return isBase64EncodedPng(val);
  }

  private isTextLegal(val: string): boolean {
    return isNonEmptyString(val);
  }

}
