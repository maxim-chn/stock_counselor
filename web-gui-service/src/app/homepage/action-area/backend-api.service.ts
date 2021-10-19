import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subscriber } from 'rxjs';

import { ApplicativeUser } from '../user';
import { UserService } from '../user.service';

@Injectable({
  providedIn: 'root'
})
export class BackendApiService {

  static getError(functionName: string, message: string): Error {
    let errMsg = `${BackendApiService.name} -- ${functionName}() -- ${message}`;
    return Error(errMsg);
  }

  public className: string;

  private hostname: string;
  private port: string;
  private protocol: string;

  constructor(
    private httpClient: HttpClient,
    private userService: UserService
    ) {
    this.className = BackendApiService.name;
    this.hostname = "localhost";
    this.port = "3000";
    this.protocol = "http";
  }

  public calculateInvestmentRecommendation(): Observable<string> {
    let headers = this.headersForCalculateInvestmentRecommendationRequest();
    let parameters = this.parametersForCalculateInvestmentRecommendationRequest();
    let requestUrl = this.urlForCalculateInvestmentRecommendationRequest();
    let result = new Observable<string>(subscriber => {
      let futureResponse = this.httpClient.get<string>(requestUrl, { headers: headers, params: parameters });
      futureResponse.subscribe({
        next: val => this.responseForCalculateInvestmentRecommendationRequest(val, subscriber),
        error: err => this.failedResponseForCalculateInvestmentRecommendationRequest(err, subscriber)
      });
    });
    return result;
  }
  
  public collectStockData(stockAcronym: string): Observable<string> {
    let headers = this.headersForCollectStockDataRequest();
    let parameters = this.parametersForCollectStockDataRequest(stockAcronym);
    let requestUrl = this.urlForCollectStockDataRequest();
    let result = new Observable<string>(subscriber => {
      let futureResponse = this.httpClient.get<string>(requestUrl, { headers: headers, params: parameters });
      futureResponse.subscribe({
        next: val => this.responseForCollectStockDataRequest(val, subscriber),
        error: err => this.failedResponseForCollectStockDataRequest(err, subscriber)
      });
    });
    return result;
  }

  public login(user: ApplicativeUser): Observable<ApplicativeUser> {
    let headers = this.headersForLoginRequest();
    let parameters = this.parametersForLoginRequest(user);
    let requestUrl = this.urlForLoginRequest();
    let result = new Observable<ApplicativeUser>(subscriber => {
      let futureResponse = this.httpClient.get<string>(requestUrl, { headers: headers, params: parameters });
      futureResponse.subscribe({
        next: val => this.responseForLoginRequest(val, subscriber),
        error: err => this.failedResponseForLoginRequest(err, subscriber)
      });
    });
    return result;
  }

  public signup(user: ApplicativeUser): Observable<ApplicativeUser> {
    let headers = this.headersForSignupRequest();
    let parameters = this.parametersForSignupRequest(user);
    let requestUrl = this.urlForSignupRequest();
    let result = new Observable<ApplicativeUser>(subscriber => {
      let futureResponse = this.httpClient.get<string>(requestUrl, { headers: headers, params: parameters });
      futureResponse.subscribe({
        next: val => this.responseForSignupRequest(val, subscriber),
        error: err => this.failedResponseForSignupRequest(err, subscriber)
      });
    });
    return result;
  }

  private applicativeUserFromJson(val: string): ApplicativeUser {
    try {
      let result = new ApplicativeUser();
      let userJson = JSON.parse(val);
      result.setAmountOfCompaniesToInvest(userJson.amount_of_companies_to_invest);
      result.setAvatar(userJson.avatar.alt_text, userJson.avatar.img_src);
      result.setEmail(userJson.email);
      result.setFirstName(userJson.first_name);
      result.setLastName(userJson.last_name);
      return result;
    }
    catch (err) {
      let errMsg = `Failed to parse stringified json to ApplicativeUser.\nStringified json:\t${val}`;
      throw BackendApiService.getError("applicativeUserFromJson", errMsg);
    }
  }

  private _applicativeUserToParams(user: ApplicativeUser): HttpParams {
    let result = new HttpParams();
    result.append("fist_name", user.firstName);
    result.append("last_name", user.lastName);
    result.append("email", user.email);
    return result;
  }

  private _baseUrlForBackendRequest(): string {
    let result = `${this.protocol}://${this.hostname}:${this.port}`;
    return result;
  }

  private headersForCalculateInvestmentRecommendationRequest(): HttpHeaders {
    let result = new HttpHeaders();
    result.append("Accept", "text/plain");
    return result;
  }

  private headersForCollectStockDataRequest(): HttpHeaders {
    let result = new HttpHeaders();
    result.append("Accept", "text/plain");
    return result;
  }

  private headersForLoginRequest(): HttpHeaders {
    let result = new HttpHeaders();
    result.append("Accept", "application/json");
    return result;
  }

  private headersForSignupRequest(): HttpHeaders {
    let result = new HttpHeaders();
    result.append("Accept", "application/json");
    return result;
  }

  private failedResponseForCalculateInvestmentRecommendationRequest(err: Error, subscriber: Subscriber<string>): void {
    let errMsg = `Failed.\n${err}`;
    let updatedError = BackendApiService.getError("failedResponseForCalculateInvestmentRecommendationRequest", errMsg);
    subscriber.error(updatedError);
  }

  private failedResponseForCollectStockDataRequest(err: Error, subscriber: Subscriber<string>): void {
    let errMsg = `Failed.\n${err}`;
    let updatedError = BackendApiService.getError("failedResponseForCollectStockDataRequest", errMsg);
    subscriber.error(updatedError);
  }

  private failedResponseForLoginRequest(err: Error, subscriber: Subscriber<ApplicativeUser>): void {
    let errMsg = `Failed.\n${err}`;
    let updatedError = BackendApiService.getError("failedResponseForLoginRequest", errMsg);
    subscriber.error(updatedError);
  }

  private failedResponseForSignupRequest(err: Error, subscriber: Subscriber<ApplicativeUser>): void {
    let errMsg = `Failed.\n${err}`;
    let updatedError = BackendApiService.getError("failedResponseForSignupRequest", errMsg);
    subscriber.error(updatedError);
  }

  private parametersForCalculateInvestmentRecommendationRequest(): HttpParams {
    let result = new HttpParams();
    let user = this.userService.user;
    result.append("user_id", user.email);
    return result;
  }

  private parametersForCollectStockDataRequest(val: string): HttpParams {
    let result = new HttpParams();
    result.append("stock_acronym", val);
    return result;
  }

  private parametersForLoginRequest(user: ApplicativeUser): HttpParams {
    let result = this._applicativeUserToParams(user);
    return result;
  }

  private parametersForSignupRequest(user: ApplicativeUser): HttpParams {
    let result = this._applicativeUserToParams(user);
    return result;
  }

  private responseForCalculateInvestmentRecommendationRequest(val: string, subscriber: Subscriber<string>): void {
    subscriber.next(val);
  }

  private responseForCollectStockDataRequest(val: string, subscriber: Subscriber<string>): void {
    subscriber.next(val);
  }

  private responseForLoginRequest(val: string, subscriber: Subscriber<ApplicativeUser>): void {
    try {
      let loggedInUser = this.applicativeUserFromJson(val);
      subscriber.next(loggedInUser);
    }
    catch (err) {
      let errMsg = "Failed to map JSON from server to ApplicativeUser.";
      errMsg += `\nMapping error:\t${err}`;
      errMsg += `\nResponse body from server:\t${val}`;
      let updatedError = BackendApiService.getError("responseForLoginRequest", errMsg);
      subscriber.error(updatedError);
    }
  }

  private responseForSignupRequest(val: string, subscriber: Subscriber<ApplicativeUser>): void {
    try {
      let signedUpUser = this.applicativeUserFromJson(val);
      subscriber.next(signedUpUser);
    }
    catch (err) {
      let errMsg = "Failed to map JSON from server to ApplicativeUser.";
      errMsg += `\nMapping error:\t${err}`;
      errMsg += `\nResponse body from server:\t${val}`;
      let updatedError = BackendApiService.getError("responseForSignupRequest", errMsg);
      subscriber.error(updatedError);
    }
  }

  private urlForCalculateInvestmentRecommendationRequest(): string {
    let baseUrl = this._baseUrlForBackendRequest();
    let result = `${baseUrl}/calculate_investment_recommendation`;
    return result;
  }

  private urlForCollectStockDataRequest(): string {
    let baseUrl = this._baseUrlForBackendRequest();
    let result = `${baseUrl}/collect_stock_data`;
    return result;
  }

  private urlForLoginRequest(): string {
    let baseUrl = this._baseUrlForBackendRequest();
    let result = `${baseUrl}/applicative_users`;
    return result;
  }

  private urlForSignupRequest(): string {
    let baseUrl = this._baseUrlForBackendRequest();
    let result = `${baseUrl}/applicative_users/new`;
    return result;
  }
}
