import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { BackendApiService } from '../backend-api.service';

import { CalculateInvestmentRecommendationRequestContainerDirective }
  from './calculate-investment-recommendation-request-container.directive';
import { CalculateInvestmentRecommendationRequestErrorContainerDirective }
  from './calculate-investment-recommendation-request-error-container.directive';
import { CalculateInvestmentRecommendationResponseContainerDirective }
  from './calculate-investment-recommendation-response-container.directive';

@Component({
  selector: 'action-area-calculate-investment-recommendation',
  templateUrl: './calculate-investment-recommendation.component.html',
  styleUrls: ['./calculate-investment-recommendation.component.sass']
})
export class CalculateInvestmentRecommendationComponent implements OnInit {

  public className: string;
  public errorMessage: string;
  public responseMessage: string;

  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private requestContainerDirective: CalculateInvestmentRecommendationRequestContainerDirective,
    private requestErrorContainerDirective: CalculateInvestmentRecommendationRequestErrorContainerDirective,
    private responseContainerDirective: CalculateInvestmentRecommendationResponseContainerDirective
  ) {
    this.errorMessage = "No error";
    this.responseMessage = "No response";
    this.className = CalculateInvestmentRecommendationComponent.name;
  }

  ngOnInit(): void {
    this.displayRequestContainer();
  }

  public dismissErrorMessage(): void {
    this.displayRequestContainer();
  }

  public dismissResponseMessage(): void {
    this.displayRequestContainer();
  }

  public submit(): void {
    this.backendApiService.calculateInvestmentRecommendation().subscribe({
      next: val => this.nextBackendResponse(val),
      error: err => this.backendApiServiceError(err)
    });
  }

  private backendApiServiceError(err: Error): void {
    let errMsgToDisplay = "Request to backend server with calculate investment recommendation has failed.";
    this.displayRequestErrorContainer(errMsgToDisplay);
    let errMsg = `${this.backendApiService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "backendApiServiceError", errMsg);
  }

  private displayRequestContainer(): void {
    this.errorMessage = "No error";
    this.responseMessage = "No response";
    this.requestContainerDirective.show();
    this.requestErrorContainerDirective.hide();
    this.responseContainerDirective.hide();
  }

  private displayRequestErrorContainer(errorMessage: string): void {
    this.errorMessage = errorMessage;
    this.responseMessage = "No response";
    this.requestContainerDirective.hide();
    this.requestErrorContainerDirective.show();
    this.responseContainerDirective.hide();
  }

  private displayResponseContainer(responseMessage: string): void {
    this.errorMessage = "No error";
    this.responseMessage = responseMessage;
    this.requestContainerDirective.hide();
    this.requestErrorContainerDirective.hide();
    this.responseContainerDirective.show();
  }

  private nextBackendResponse(val: string): void {
    let responseMsgToDisplay = `Response from backend server:\n${val}`;
    this.displayResponseContainer(responseMsgToDisplay);
  }

}
