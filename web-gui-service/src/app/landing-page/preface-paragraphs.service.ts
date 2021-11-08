import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PrefaceParagraphsService {

  private paragraphs: Array<string>;
  
  constructor() {
    this.paragraphs = [
      "Gamblers speculate with money and live when the money allows it.",
      "Investors live with the risk."
    ]
  }

  public getParagraphs(): Observable<string[]> {
    return of(this.paragraphs);
  }
}
