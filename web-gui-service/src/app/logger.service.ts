import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoggerService {

  constructor() { }

  public debug(className: string, functionName: string, message: string): void {
    let toLog = this.formatMessage(className, functionName, message);
    console.debug(toLog);
  }

  public error(className: string, functionName: string, message: string): void {
    let toLog = this.formatMessage(className, functionName, message);
    console.error(toLog);
  }
  
  public info(className: string, functionName: string, message: string): void {
    let toLog = this.formatMessage(className, functionName, message);
    console.info(toLog);
  }

  private formatMessage(className: string, functionName: string, message: string): string {
    let dateTime = new Date().toLocaleTimeString();
    let result = `${dateTime}:\t${className} -- ${functionName}() -- ${message}`;
    return result;
  }
}
