import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from '../../logger.service';

import { ApplicativeUser } from '../user';
import { ApplicativeUserState } from '../user-state';
import { UserService } from '../user.service';

import {
  initialUserSummaryContainerClasses,
  hideUserSummaryContainer,
  showUserSummaryContainer,
  WithUserSummaryContainer
} from "./with-user-summary-container";

import {
  intialUserSummaryErrorContainerClasses,
  hideUserSummaryErrorContainer,
  showUserSummaryErrorContainer,
  WithUserSummaryErrorContainer,
} from "./with-user-summary-error-container";

@Component({
  selector: 'app-homepage-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.sass']
})
export class DashboardComponent implements OnDestroy, OnInit, WithUserSummaryContainer, WithUserSummaryErrorContainer {

  public animationTimeout: number;
  public className: string;
  public errorMessage: string;
  public title: string;
  public user: ApplicativeUser;
  @Input() userSummaryContainerClasses: Array<string>;
  @Input() userSummaryErrorContainerClasses: Array<string>;

  private userState: Subscription;
  
  constructor(private loggerService: LoggerService, private userService: UserService) {
    this.animationTimeout = 100;
    this.className = DashboardComponent.name;
    this.errorMessage = "Un-authenticated user has no details";
    this.title = "User summary";
    this.user = new ApplicativeUser();
    this.userSummaryContainerClasses = initialUserSummaryContainerClasses();
    this.userSummaryErrorContainerClasses = intialUserSummaryErrorContainerClasses();
    this.userState = new Subscription();
  }

  ngOnDestroy(): void {
    this.userState.unsubscribe();
  }

  ngOnInit(): void {
    hideUserSummaryContainer(this);
    showUserSummaryErrorContainer(this);
    this.userService.state.subscribe({
      next: val => this.userStateChanged(val),
      error: err => this.userServiceError(err)
    });
  }
  
  private userServiceError(err: Error): void {
    let errMsg = `${this.userService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "userServiceError", errMsg);
  }
  
  private userStateChanged(val: ApplicativeUserState): void {
    if (val == ApplicativeUserState.LOGGED_IN) {
      this.user = this.userService.user;
      hideUserSummaryErrorContainer(this);
      showUserSummaryContainer(this);
    }
    else if (val == ApplicativeUserState.ANONYMOUS || ApplicativeUserState.LOGGED_OUT) {
      this.user = this.userService.user;
      this.errorMessage = "Un-authenticated user has no details";
      hideUserSummaryContainer(this);
      showUserSummaryErrorContainer(this);
    }
    else {
      let errMsg = "Unexpected ApplicativeUserState value.";
      this.userServiceError(new Error(errMsg));
      this.errorMessage = "The backend has not processed authentication request as expected.";
      hideUserSummaryContainer(this);
      showUserSummaryErrorContainer(this);
    }
  }
}
