import { Component, Input, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { BackendApiService } from '../backend-api.service';

import {
  hideRequestContainer,
  initialRequestContainerClasses,
  showRequestContainer,
  WithRequestContainer
} from "../with-request-container";

import {
  hideRequestErrorContainer,
  initialRequestErrorContainerClasses,
  showRequestErrorContainer,
  WithRequestErrorContainer
} from "../with-request-error-container";

import {
  hideResponseContainer,
  initialResponseContainerClasses,
  showResponseContainer,
  WithResponseContainer
} from "../with-response-container";

@Component({
  selector: 'action-area-calculate-investment-recommendation',
  templateUrl: './calculate-investment-recommendation.component.html',
  styleUrls: ['./calculate-investment-recommendation.component.sass']
})
export class CalculateInvestmentRecommendationComponent implements
  OnInit, WithRequestContainer, WithRequestErrorContainer, WithResponseContainer {
  
  
  public animationTimeout: number;
  public className: string;
  public componentDescription: Array<string>;
  public errorMessage: string;
  @Input() requestContainerClasses: Array<string>;
  @Input() requestErrorContainerClasses: Array<string>;
  @Input() responseContainerClasses: Array<string>;
  public responseMessage: string;
  public title: string;

  constructor(private backendApiService: BackendApiService, private loggerService: LoggerService) {
    this.animationTimeout = 100;
    this.className = CalculateInvestmentRecommendationComponent.name;
    this.componentDescription = Array<string>();
    this.errorMessage = "No error";
    this.requestContainerClasses = initialRequestContainerClasses();
    this.requestErrorContainerClasses = initialRequestErrorContainerClasses();
    this.responseContainerClasses = initialResponseContainerClasses();
    this.responseMessage = "No response";
    this.title = "Get investment recommendation";
    this.initComponentDescription();
  }

  ngOnInit(): void {
    hideRequestErrorContainer(this);
    hideResponseContainer(this);
    showRequestContainer(this);
  }

  public dismissErrorMessage(): void {
    this.errorMessage = "No error";
    hideRequestErrorContainer(this);
    showRequestContainer(this);
  }

  public dismissResponseMessage(): void {
    this.responseMessage = "No response";
    hideResponseContainer(this);
    showRequestContainer(this);
  }

  public submit(): void {
    hideRequestContainer(this);
    this.backendApiService.calculateInvestmentRecommendation().subscribe({
      next: val => this.nextBackendResponse(val),
      error: err => this.backendApiServiceError(err)
    });
  }

  private backendApiServiceError(err: Error): void {
    let errMsg = `${this.backendApiService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "backendApiServiceError", errMsg);
    this.errorMessage = "Request to backend server with calculate investment recommendation has failed.";
    showRequestErrorContainer(this);
  }

  private initComponentDescription(): void {
    this.componentDescription = [
      "Automated stock counselor will go over the available financial reports.",
      "It will compare the data against your investment preferences.",
      "The comparison will be evaluated from 0 to 1.",
      "The higher the score, the more suitable the company to invest into"
    ];
  }

  private nextBackendResponse(val: string): void {
    this.responseMessage = val;
    showResponseContainer(this);
  }

}
