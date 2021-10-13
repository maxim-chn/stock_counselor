import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { User } from 'src/app/homepage/user';
import { UserService } from 'src/app/homepage/user.service';

@Component({
  selector: 'app-homepage-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.sass']
})
export class DashboardComponent implements OnInit {

  public user: User;
  
  constructor(private loggerService: LoggerService, private userService: UserService) {
    this.user = new User();
  }

  ngOnInit(): void {
    this.userService.getUser().subscribe({
      next: val => this.nextUser(val),
      error: err => this.userServiceError(err)
    });
  }

  private nextUser(val: User): void {
    this.user = val;
  }

  private userServiceError(err: Error): void {
    let errMsg = `Failed.\n${err}`;
    this.loggerService.error(DashboardComponent.name, "userServiceError", errMsg);
  }

}
