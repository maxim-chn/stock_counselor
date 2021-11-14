import { isBase64EncodedPng, isEmail, isInteger, isNonEmptyString } from "src/app/validations";

class Avatar {

  static throwError(functionName: string, message: string): void {
    let errMsg = `${Avatar.name} -- ${functionName}() -- ${message}`;
    throw Error(errMsg);
  }
  
  static withAllAttributes(altText: string, imgSrc: string): Avatar {
    let result = new Avatar();
    try {
      result.setAltText(altText);
      result.setImgSrc(imgSrc);
    } catch (err) {
      let errMsg = `Failed.\n${err}`;
      Avatar.throwError("withAllAttributes", errMsg);
    }
    return result;
  }

  public altText: string;
  public imgSrc: string;

  constructor() {
    this.altText = "To be replaced";
    this.imgSrc = "To be replaced";
  }

  private setAltText(val: string): void {
    if (this.isAltTextLegal(val)) {
      this.altText = val;
    }
    else {
      Avatar.throwError("setAltText", "Expected a non empty string.");
    }
  }

  private setImgSrc(val: string): void {
    if (this.isImgSrcLegal(val)) {
      this.imgSrc = val;
    }
    else {
      Avatar.throwError("setImgSrc", "Expected an encoded PNG.");
    }
  }

  private isAltTextLegal(val: string): boolean {
    return isNonEmptyString(val);
  }

  private isImgSrcLegal(val: string): boolean {
    return isBase64EncodedPng(val);
  }
}

export class ApplicativeUser {

  static throwError(functionName: string, message: string): void {
    let errMsg = `${ApplicativeUser.name} -- ${functionName}() -- ${message}`;
    throw Error(errMsg);
  }

  static withAllAttributes(
    avatarAltText: string,
    avatarImgSrc: string,
    email: string,
    firstName: string,
    lastName: string
    ): ApplicativeUser {
      let result = new ApplicativeUser();
      try {
        let avatar = Avatar.withAllAttributes(avatarAltText, avatarImgSrc);
        result.setAvatar(avatar);
        result.setEmail(email);
        result.setFirstName(firstName);
        result.setLastName(lastName);
      } catch (err) {
        let errMsg = `Failed.\n${err}`;
        ApplicativeUser.throwError("withAllAttributes", errMsg);
      }
      return result;
  }

  public avatar: Avatar;
  public email: string;
  public firstName: string;
  public lastName: string;

  constructor() {
    this.avatar = new Avatar();
    this.email = "To be replaced";
    this.firstName = "To be replaced";
    this.lastName = "To be replaced";
  }

  public setAvatar(...args: any[]): void {
    let avatar: Avatar;
    if (args.length == 2) {
      avatar = Avatar.withAllAttributes(args[0], args[1]);
      this._setAvatar(avatar);
    }
    else if (args.length == 1) {
      this._setAvatar(args[0]);
    }
    else {
      ApplicativeUser.throwError("setAvatar", "Expected 1 argument or 2 arguments.");
    }
  }

  public setEmail(val: string): void {
    if (this.isEmailLegal(val)) {
      this.email = val;
    }
    else {
      ApplicativeUser.throwError("setEmail", "Expected an email address.");
    }
  }

  public setFirstName(val: string): void {
    if (this.isFirstNameLegal(val)) {
      this.firstName = val;
    }
    else {
      ApplicativeUser.throwError("setFirstName", "Expected a non empty string.");
    }
  }

  public setLastName(val: string): void {
    if (this.isLastNameLegal(val)) {
      this.lastName = val;
    }
    else {
      ApplicativeUser.throwError("setLastName", "Expected a non empty string.");
    }
  }

  private _setAvatar(val: Avatar): void {
    if (this.isAvatarLegal(val)) {
      this.avatar = val;
    }
    else {
      ApplicativeUser.throwError("_setAvatar", "Expected an object Avatar.");
    }
  }

  private isAvatarLegal(val: Avatar): boolean {
    if (val) {
      return true;
    }
    return false;
  }

  private isEmailLegal(val: string): boolean {
    if (isEmail(val)) {
      return true;
    }
    return false;
  }

  private isFirstNameLegal(val: string): boolean {
    if (isNonEmptyString(val)) {
      return true;
    }
    return false;
  }

  private isLastNameLegal(val: string): boolean {
    if (isNonEmptyString(val)) {
      return true;
    }
    return false;
  }
}
