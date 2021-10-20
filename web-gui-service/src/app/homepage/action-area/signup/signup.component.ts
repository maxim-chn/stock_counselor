import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { ApplicativeUser } from '../../user';
import { UserService } from '../../user.service';

import { BackendApiService } from '../backend-api.service';

import { SignupRequestContainerDirective } from './signup-request-container.directive';
import { SignupRequestErrorContainerDirective } from './signup-request-error-container.directive';

@Component({
  selector: 'action-area-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.sass']
})
export class SignupComponent implements OnInit {

  public className: string;
  public email: string;
  public errorMessage: string;
  public firstName: string;
  public lastName: string;
  
  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private requestContainerDirective: SignupRequestContainerDirective,
    private requestErrorContainerDirective: SignupRequestErrorContainerDirective,
    private UserService: UserService
  ) {
    this.className = SignupComponent.name;
    this.email = "No value";
    this.errorMessage = "No error";
    this.firstName = "No value";
    this.lastName = "No value";
  }

  ngOnInit(): void {
    this.displayRequestForm();
  }

  public dismissErrorMessage(): void {
    this.displayRequestForm();
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

  public submit(): void {
    let userToSubmit = new ApplicativeUser();

    try {
      userToSubmit.setEmail(this.email);
      userToSubmit.setFirstName(this.firstName);
      userToSubmit.setLastName(this.lastName);
    }
    catch (err) {
      let errMsg = `Failed to update ApplicativeUser object attributes.\n${err}`;
      this.loggerService.error(this.className, "submit", errMsg);
      this.displayError("You have entered illegal values. Please try again.");
      return;
    }

    this.backendApiService.signup(userToSubmit).subscribe({
      next: val => this.nextSignedUpUser(val),
      error: err => this.backendApiSignupRequestError(err)
    });
  }

  private backendApiSignupRequestError(err: Error): void {
    let errMsg = `Failed to signup against the backend server.\n${err}`;
    this.loggerService.error(this.className, "backendApiSginupRequestError", errMsg);
    let displayErrMsg = "We have failed to contact the backend server";
    this.displayError(displayErrMsg);
  }

  private displayError(val: string): void {
    this.errorMessage = val;
    this.requestContainerDirective.hide();
    this.requestErrorContainerDirective.show();
  }

  private displayRequestForm(): void {
    this.errorMessage = "No error";
    this.requestContainerDirective.show();
    this.requestErrorContainerDirective.hide();
  }

  private nextSignedUpUser(val: ApplicativeUser): void {
    this.UserService.hasSignedUp(val);
  }

}
