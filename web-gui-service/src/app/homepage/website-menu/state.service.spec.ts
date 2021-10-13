import { TestBed } from '@angular/core/testing';

import { WebsiteMenuStateService } from './state.service';

describe('WebsiteMenuStateService', () => {
  let service: WebsiteMenuStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WebsiteMenuStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
