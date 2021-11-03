import { Component, Input, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';

import { ApplicativeUser } from '../../user';
import { ApplicativeUserState } from '../../user-state';
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
  public title: string;

  private userState: Subscription;
  
  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private userService: UserService
  ) {
    super();
    this.animationTimeout = 100;
    this.className = SignupComponent.name;
    this.errorMessage = "No error";
    this.requestContainerClasses = initialRequestContainerClasses();
    this.requestErrorContainerClasses = initialRequestErrorContainerClasses();
    this.title = "Please enter your registration details below";
    this.userState = new Subscription();
  }

  ngOnInit(): void {
    hideRequestErrorContainer(this);
    showRequestContainer(this);
    this.userState = this.userService.state.subscribe({
        next: val => this.userStateChanged(val),
        error: err => this.userServiceError(err)
      }
    );
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
    this.userService.hasSignedUp(val);
  }

  private userServiceError(err: Error): void {
    let errMsg = `${this.userService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "userServiceError", errMsg); 
  }

  private userStateChanged(val: ApplicativeUserState): void {
    if (val == ApplicativeUserState.LOGGED_IN) {
      hideRequestErrorContainer(this);
      hideRequestContainer(this);
    }
    else if (val == ApplicativeUserState.LOGGED_OUT || val == ApplicativeUserState.ANONYMOUS) {
      hideRequestErrorContainer(this);
      showRequestContainer(this);
    }
    else {
      let errMsg = `Unexpected ApplicativeUserState has been returned.\nVal:\t${val}`;
      this.userServiceError(new Error(errMsg));
    }
  }

}
