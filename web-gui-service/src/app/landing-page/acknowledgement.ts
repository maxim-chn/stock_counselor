import { isNonEmptyString } from "../validations";

export class Acknowledgement {

  static throwError(functionName: string, message: string): void {
    let errMsg = `${Acknowledgement.name} -- ${functionName}() -- ${message}`;
    throw Error(errMsg);
  }

  static withAllAttributes(paragraphs: Array<string>, title: string): Acknowledgement {
    let result = new Acknowledgement();
    try {
      result.setParagraphs(paragraphs);
      result.setTitle(title);
    } catch (err) {
      let errMsg = `Failed.\n${err}`;
      Acknowledgement.throwError("withAllAttributes", errMsg);
    }
    return result;
  }
  
  public paragraphs: Array<String>;
  public title: String;

  public constructor() {
    this.paragraphs = [];
    this.title = "Value should have been updated";
  }

  public setParagraphs(val: Array<string>): void {
    if (this.isParagraphsLegal(val)) {
      this.paragraphs = val;
    }
    else {
      Acknowledgement.throwError("setParagraphs", "Expected a non empty array of non empty strings");
    }
  }

  public setTitle(val: string): void {
    if (this.isTitleLegal(val)) {
      this.title = val;
    }
    else {
      Acknowledgement.throwError("setTitle", "Expected a non emtpy string");
    }
  }

  private isParagraphLegal(val: string): boolean {
    return isNonEmptyString(val);
  }

  private isParagraphsLegal(val: Array<string>): boolean {
    let result = false;
    for (let paragraph in val) {
      if (this.isParagraphLegal(paragraph)) {
        result = true;
      }
      else {
        return false;
      }
    }
    return result;
  }

  private isTitleLegal(val: string): boolean {
    return isNonEmptyString(val);
  }
}
