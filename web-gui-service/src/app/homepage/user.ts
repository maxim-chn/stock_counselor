import { isBase64EncodedPng, isInteger, isNonEmptyString } from "src/app/validations";

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
    amountOfCompaniesToInvest: Number,
    avatarAltText: string,
    avatarImgSrc: string,
    firstName: string,
    lastName: string
    ): ApplicativeUser {
      let result = new ApplicativeUser();
      try {
        let avatar = Avatar.withAllAttributes(avatarAltText, avatarImgSrc);
        result.setAmountOfCompaniesToInvest(amountOfCompaniesToInvest);
        result.setAvatar(avatar);
        result.setFirstName(firstName);
        result.setLastName(lastName);
      } catch (err) {
        let errMsg = `Failed.\n${err}`;
        ApplicativeUser.throwError("withAllAttributes", errMsg);
      }
      return result;
  }

  public amountOfCompaniesToInvest: Number;
  public avatar: Avatar;
  public firstName: string;
  public lastName: string;

  constructor() {
    this.avatar = new Avatar();
    this.amountOfCompaniesToInvest = 0;
    this.firstName = "To be replaced";
    this.lastName = "To be replaced";
  }

  public setAmountOfCompaniesToInvest(val: Number): void {
    if (this.isAmountOfCompaniesToInvestLegal(val)) {
      this.amountOfCompaniesToInvest = val;
    }
    else {
      ApplicativeUser.throwError("setAmountOfCompaniesToInvest", "Expected an Integer.");
    }
  }

  public setAvatar(val: Avatar): void {
    if (this.isAvatarLegal(val)) {
      this.avatar = val;
    }
    else {
      ApplicativeUser.throwError("setAvatar", "Expected an object Avatar.");
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

  public isAmountOfCompaniesToInvestLegal(val: Number): boolean {
    if (isInteger(val)) {
      return true;
    }
    return false;
  }

  public isAvatarLegal(val: Avatar): boolean {
    if (val) {
      return true;
    }
    return false;
  }

  public isFirstNameLegal(val: string): boolean {
    if (isNonEmptyString(val)) {
      return true;
    }
    return false;
  }

  public isLastNameLegal(val: string): boolean {
    if (isNonEmptyString(val)) {
      return true;
    }
    return false;
  }
}
