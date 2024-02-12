import { Injectable } from '@nestjs/common';
import { CreateNewsDto } from './dto/create-news.dto';
import { UpdateNewsDto } from './dto/update-news.dto';
import { NewsRepository } from './news.repository';

@Injectable()
export class NewsService {

  constructor(private readonly repository:NewsRepository){}

  create(createNewsDto: CreateNewsDto) {
    return 'This action adds a new news';
  }

  findAll() {
    return this.repository.findAll();
  }

  findOne(source: string) {
    return this.repository.findNewsBySource(source)
  }

  update(id: number, updateNewsDto: UpdateNewsDto) {
    return `This action updates a #${id} news`;
  }

  remove(id: number) {
    return `This action removes a #${id} news`;
  }
}
