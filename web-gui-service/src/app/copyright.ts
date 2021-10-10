import { isLink, isNonEmptyString } from "./validations";

export class Copyright {

  static throwError(functionName: string, message: string): void {
    let errMsg = `${Copyright.name} -- ${functionName}() -- ${message}`;
    throw Error(errMsg);
  }

  static withAllAttributes(description: string, link: string): Copyright {
    let result = new Copyright();
    try {
      result.setDescription(description);
      result.setLink(link);
    } catch (err) {
      let errMsg = `Failed.\n${err}`;
      Copyright.throwError("withAllAttributes", errMsg);
    }
    return result;
  }

  public description: string;
  public link: string;

  public constructor() {
    this.description = "Value should have been updated";
    this.link = "Value should have been updated";
  }

  public setDescription(val: string): void {
    if (isNonEmptyString(val)) {
      this.description = val;
    }
    else {
      Copyright.throwError("setDescription", "Expected non empty string");
    }
  }

  public setLink(val: string): void {
    if (isLink(val)) {
      this.link = val;
    }
    else {
      Copyright.throwError("setLink", "Illegal value");
    }
  }
}
