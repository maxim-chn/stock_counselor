import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';

import { UserService } from '../../user.service';
import { ApplicativeUserState } from '../../user-state';

import { InvestmentFunctionalitiesMenuStateService } from './state.service';

@Component({
  selector: 'action-area-investment-functionalities-menu',
  templateUrl: './investment-functionalities-menu.component.html',
  styleUrls: ['./investment-functionalities-menu.component.sass']
})
export class InvestmentFunctionalitiesMenuComponent implements OnDestroy, OnInit {

  public nonGuest: boolean;

  public userState: Subscription

  constructor(
    private loggerService: LoggerService,
    private menuStateService: InvestmentFunctionalitiesMenuStateService,
    private userService: UserService
  ) {
    this.nonGuest = false;
    this.userState = new Subscription();
  }

  ngOnDestroy(): void {
    this.userState.unsubscribe();
  }

  ngOnInit(): void {
    this.userState = this.userService.state.subscribe({
      next: val => this.nextUserState(val),
      error: err => this.userServiceError(err)
    });
  }

  public calculateInvestmentRecommendation(): void {
    this.menuStateService.calculateInvestmentRecommendation();
  }

  public collectStockData(): void {
    this.menuStateService.collectStockData();
  }

  private nextUserState(val: ApplicativeUserState): void {
    if (val == ApplicativeUserState.ANONYMOUS) {
      this.nonGuest = false;
    }
    else if (val == ApplicativeUserState.LOGGED_IN) {
      this.nonGuest = true;
    }
    else if (val == ApplicativeUserState.LOGGED_OUT) {
      this.nonGuest = false;
    }
    else {
      let errMsg = `Unexpected ApplicativeUserState has been returned.\nVal:\t${val}`;
      this.userServiceError(new Error(errMsg));
    }
  }

  private userServiceError(err: Error): void {
    let errMsg = `userService has failed.\n${err}`;
    this.loggerService.error(InvestmentFunctionalitiesMenuComponent.name, "userServiceError", errMsg);
  }

}
