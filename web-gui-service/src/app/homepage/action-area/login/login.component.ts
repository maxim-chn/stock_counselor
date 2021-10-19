import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { ApplicativeUser } from '../../user';
import { UserService } from '../../user.service';
import { BackendApiService } from '../backend-api.service';

import { LoginRequestContainerDirective } from './login-request-container.directive';
import { LoginRequestErrorContainerDirective } from './login-request-error-container.directive';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})
export class LoginComponent implements OnInit {

  public className: string;
  public errorMessage: string;
  
  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private requestContainerDirective: LoginRequestContainerDirective,
    private requestErrorContainerDirective: LoginRequestErrorContainerDirective,
    private userService: UserService
    ) {
      this.className = LoginComponent.name;
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
      userToSubmit.setFirstName(firstName);
      userToSubmit.setLastName(lastName);
      userToSubmit.setEmail(email);
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

  private nextLoggedInUser(val: ApplicativeUser): void {
    this.userService.hasLoggedIn(val);
  }

}
