import { TestBed } from '@angular/core/testing';

import { InvestmentFunctionalitiesMenuStateService } from './state.service';

describe('InvestmentFunctionalitiesMenuStateService', () => {
  let service: InvestmentFunctionalitiesMenuStateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InvestmentFunctionalitiesMenuStateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
