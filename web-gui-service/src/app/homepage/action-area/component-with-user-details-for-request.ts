export class ComponentWithUserDetailsForRequest {
  public email: string;
  public firstName: string;
  public lastName: string;

  constructor() {
    this.email = "No value";
    this.firstName = "No value";
    this.lastName = "No value";
  }

  public emailUpdated(event: Event): void {
    this.email = (<HTMLInputElement>event.target).value;
  }

  public firstNameUpdated(event: Event): void {
    this.firstName = (<HTMLInputElement>event.target).value;
  }

  public lastNameUpdated(event: Event): void {
    this.lastName = (<HTMLInputElement>event.target).value;
  }
}
