import { Component, Input, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { removeFromStringArray } from 'src/app/utils';

import { ApplicativeUser } from '../../user';
import { UserService } from '../../user.service';
import { BackendApiService } from '../backend-api.service';

@Component({
  selector: 'action-area-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})
export class LoginComponent implements OnInit {

  public className: string;
  public email: string;
  public errorMessage: string;
  public firstName: string;
  public lastName: string;
  public animationTimeout: number;

  @Input() requestContainerClasses: Array<string>;
  @Input() requestErrorContainerClasses: Array<string>;
  
  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private userService: UserService
    ) {
      this.animationTimeout = 100;
      this.className = LoginComponent.name;
      this.email = "No value";
      this.errorMessage = "No error";
      this.firstName = "No value";
      this.lastName = "No value";
      this.requestContainerClasses = [
        "animated",
        "non-visible-non-rendered"
      ];
      this.requestErrorContainerClasses = [
        "animated",
        "non-visible-non-rendered"
      ]
    }
    
  ngOnInit(): void {
    this.hideRequestErrorContainer();
    this.showRequestContainer();
  }

  public dismissErrorMessage(): void {
    this.hideRequestErrorContainer();
    this.showRequestContainer();
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

  public hideRequestContainer(): void {
    removeFromStringArray(this.requestContainerClasses, "rendered-visible");
    this.requestContainerClasses.push("non-visible-non-rendered");
  }

  public hideRequestErrorContainer(): void {
    removeFromStringArray(this.requestErrorContainerClasses, "rendered-visible");
    this.requestErrorContainerClasses.push("non-visible-non-rendered");
  }

  public submit(): void {
    let userToSubmit = new ApplicativeUser();
    
    try {
      userToSubmit.setFirstName(this.firstName);
      userToSubmit.setLastName(this.lastName);
      userToSubmit.setEmail(this.email);
    }
    catch (err) {
      let errMsg = `Failed to update ApplicativeUser object details.\n${err}`;
      this.loggerService.error(this.className, "submit", errMsg);
      this.displayError("You have entered illegal values. Please try again");
      return;
    }

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
    this.hideRequestContainer();
    this.showRequestErrorContainer();
  }

  private showRequestContainer(): void {
    removeFromStringArray(this.requestContainerClasses, "non-visible-non-rendered");
    this.requestContainerClasses.push("non-visible-rendered");
    setTimeout(
      () => {
        removeFromStringArray(this.requestContainerClasses, "non-visible-rendered");
        this.requestContainerClasses.push("rendered-visible");
      },
      this.animationTimeout
    );
  }

  private showRequestErrorContainer(): void {
    removeFromStringArray(this.requestErrorContainerClasses, "non-visible-non-rendered");
    this.requestErrorContainerClasses.push("non-visible-rendered");
    setTimeout(
      () => {
        removeFromStringArray(this.requestErrorContainerClasses, "non-visible-rendered");
        this.requestErrorContainerClasses.push("rendered-visible");
      },
      this.animationTimeout
    );
  }

  private nextLoggedInUser(val: ApplicativeUser): void {
    this.userService.hasLoggedIn(val);
  }

}
