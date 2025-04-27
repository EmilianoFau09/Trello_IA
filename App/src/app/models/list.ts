import {Card} from './card';

export interface List {
  idList?: string,
  title: string,
  description: string,
  cards?: Card[];
}
