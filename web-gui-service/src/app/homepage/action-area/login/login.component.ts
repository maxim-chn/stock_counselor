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
  selector: 'action-area-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})
export class LoginComponent extends ComponentWithUserDetailsForRequest implements
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
      this.className = LoginComponent.name;
      this.errorMessage = "No error";
      this.requestContainerClasses = initialRequestContainerClasses();
      this.requestErrorContainerClasses = initialRequestErrorContainerClasses();
      this.title = "Please enter your authentication details below";
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

  ngOnDestroy(): void {
    hideRequestErrorContainer(this);
    hideRequestContainer(this);
    this.userState.unsubscribe();
  }

  public dismissErrorMessage(): void {
    this.errorMessage = "No error";
    hideRequestErrorContainer(this);
    showRequestContainer(this);
  }

  public submit(): void {
    let userToSubmit = new ApplicativeUser();
    
    // try {
    //   userToSubmit.setFirstName(this.firstName);
    //   userToSubmit.setLastName(this.lastName);
    //   userToSubmit.setEmail(this.email);
    // }
    // catch (err) {
    //   let errMsg = `Failed to update ApplicativeUser object details.\n${err}`;
    //   this.loggerService.error(this.className, "submit", errMsg);
    //   this.displayError("You have entered illegal values. Please try again");
    //   return;
    // }

    this.backendApiService.login(userToSubmit).subscribe({
      next: val => this.nextLoggedInUser(val),
      error: err => this.backendApiLoginRequestError(err)
    });
  }

  private backendApiLoginRequestError(err: Error): void {
    let errMsg = `Login request to the backend server has failed.\n${err}`;
    this.loggerService.error(this.className, "backendApiLoginRequestError", errMsg);
    let displayErrMsg = "We have failed to contact the backend server";
    this.displayError(displayErrMsg);
  }

  private displayError(val: string): void {
    this.errorMessage = val;
    hideRequestContainer(this);
    showRequestErrorContainer(this);
  }

  private nextLoggedInUser(val: ApplicativeUser): void {
    this.userService.hasLoggedIn(val);
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
