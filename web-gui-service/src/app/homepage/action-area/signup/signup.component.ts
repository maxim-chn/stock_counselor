import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { ApplicativeUser } from '../../user';
import { UserService } from '../../user.service';

import { BackendApiService } from '../backend-api.service';

import { SignupRequestContainerDirective } from './signup-request-container.directive';
import { SignupRequestErrorContainerDirective } from './signup-request-error-container.directive';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.sass']
})
export class SignupComponent implements OnInit {

  public className: string;
  public errorMessage: string;
  
  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private requestContainerDirective: SignupRequestContainerDirective,
    private requestErrorContainerDirective: SignupRequestErrorContainerDirective,
    private UserService: UserService
  ) {
    this.className = SignupComponent.name;
    this.errorMessage = "No error";
  }

  ngOnInit(): void {
    this.displayRequestForm();
  }

  public dismissErrorMessage(): void {
    this.displayRequestForm();
  }

  public submit(firstName: string, lastName: string, email: string): void {
    let userToSubmit = new ApplicativeUser();

    try {
      userToSubmit.email = email;
      userToSubmit.firstName = firstName;
      userToSubmit.lastName = lastName;
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
    this.displayError(errMsg);
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
