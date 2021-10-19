import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';

import { ApplicativeUser } from 'src/app/homepage/user';
import { ApplicativeUserState } from '../user-state';
import { UserService } from 'src/app/homepage/user.service';

@Component({
  selector: 'app-homepage-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.sass']
})
export class DashboardComponent implements OnDestroy, OnInit {

  public className: string;
  public user: ApplicativeUser;

  private userState: Subscription;
  
  constructor(private loggerService: LoggerService, private userService: UserService) {
    this.className = DashboardComponent.name;
    this.user = new ApplicativeUser();
    this.userState = new Subscription();
  }

  ngOnDestroy(): void {
    this.userState.unsubscribe();
  }

  ngOnInit(): void {
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
    this.user = this.userService.user;
  }
}
