import { Component, Input, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';
import { isStockAcronymLegal } from 'src/app/validations';

import { BackendApiService } from '../backend-api.service';
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
import {
  hideResponseContainer,
  initialResponseContainerClasses,
  showResponseContainer,
  WithResponseContainer
} from '../with-response-container';

@Component({
  selector: 'action-area-collect-stock-data',
  templateUrl: './collect-stock-data.component.html',
  styleUrls: ['./collect-stock-data.component.sass']
})
export class CollectStockDataComponent implements
  OnInit, WithRequestContainer, WithRequestErrorContainer, WithResponseContainer {

  public animationTimeout: number;
  public className: string;
  public componentDescription: Array<string>;
  public errorMessage: string;
  @Input() requestContainerClasses: Array<string>;
  @Input() requestErrorContainerClasses: Array<string>;
  @Input() responseContainerClasses: Array<string>;
  public responseMessage: string;
  public stockAcronym: string;
  public title: string;

  constructor (private backendApiService: BackendApiService, private loggerService: LoggerService) {
    this.animationTimeout = 100;
    this.className = CollectStockDataComponent.name;
    this.componentDescription = [];
    this.errorMessage = "No error";
    this.responseMessage = "No response";
    this.stockAcronym = "No value";
    this.title = "Collect financial data";
    this.initComponentDescription();
    this.requestContainerClasses = initialRequestContainerClasses();
    this.requestErrorContainerClasses = initialRequestErrorContainerClasses();
    this.responseContainerClasses = initialResponseContainerClasses();
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
    
    if (isStockAcronymLegal(this.stockAcronym)) {
      this.backendApiService.collectStockData(this.stockAcronym).subscribe({
        next: val => this.nextBackendResponse(val),
        error: err => this.backendApiServiceError(err)
      });
      this.stockAcronym = "No value";
    }
    
    else {
      this.errorMessage = "You have used a wrong stock acronym format.";
      this.errorMessage += "\nThe right format, for example, is msft or MSFT.";
      showRequestErrorContainer(this);
    }
  }

  public stockAcronymUpdated(event: Event): void {
    this.stockAcronym = (<HTMLInputElement>event.target).value;
  }

  private backendApiServiceError(err: Error): void {
    let errMsg = `${this.backendApiService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "backendApiServiceError", errMsg);
    this.errorMessage = "Backend server has failed to respond.\nPlease try again";
    hideRequestErrorContainer(this);
    showRequestErrorContainer(this);
  }

  private initComponentDescription(): void {
    this.componentDescription = [
      "Automated stock counselor accepts stock symbols, i.e. PBCT, as an input.",
      "Once you dispatch a request, the backend server contacts U.S. Securities And Exchange Commission (SEC).",
      "SEC offers an official database, named EDGAR, as a source for the companies' financial data.",
      "The data that stock counselor retrieves from EDGAR is arranged and mapped into the JSON format.",
      "The format makes the data accessible for our recommendation algorithm."
    ]
  }

  private nextBackendResponse(val: string): void {
    this.responseMessage = val;
    showResponseContainer(this);
  }

}
