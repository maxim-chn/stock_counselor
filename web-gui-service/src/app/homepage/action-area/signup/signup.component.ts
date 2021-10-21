import { Component, Input, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { ApplicativeUser } from '../../user';
import { UserService } from '../../user.service';

import { BackendApiService } from '../backend-api.service';
import { ComponentWithUserDetailsForRequest } from '../component-with-user-details-for-request';
import {
  hideRequestContainer,
  initialRequestContainerClasses,
  showRequestContainer,
  WithRequestContainer
} from '../with-request-container';
import {
  hideRequestErrorContainer,
  initialRequestErrorContainerClasses,
  showRequestErrorContainer,
  WithRequestErrorContainer
} from '../with-request-error-container';

@Component({
  selector: 'action-area-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.sass']
})
export class SignupComponent extends ComponentWithUserDetailsForRequest implements
OnInit, WithRequestContainer, WithRequestErrorContainer {

  public animationTimeout: number;
  public className: string;
  public errorMessage: string;
  
  @Input() requestContainerClasses: Array<string>;
  @Input() requestErrorContainerClasses: Array<string>;
  
  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private UserService: UserService
  ) {
    super();
    this.animationTimeout = 100;
    this.className = SignupComponent.name;
    this.errorMessage = "No error";
    this.requestContainerClasses = initialRequestContainerClasses();
    this.requestErrorContainerClasses = initialRequestErrorContainerClasses();
  }

  ngOnInit(): void {
    hideRequestErrorContainer(this);
    showRequestContainer(this);
  }

  public dismissErrorMessage(): void {
    this.errorMessage = "No error";
    hideRequestErrorContainer(this);
    showRequestContainer(this);
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
    hideRequestContainer(this);
    console.log("After hideRequestContainer");
    showRequestErrorContainer(this);
  }

  private nextSignedUpUser(val: ApplicativeUser): void {
    this.UserService.hasSignedUp(val);
  }

}
