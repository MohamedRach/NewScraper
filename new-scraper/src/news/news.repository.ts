import { Injectable } from "@nestjs/common";
import { DynamoDBClient, ScanCommand, GetItemCommand } from "@aws-sdk/client-dynamodb";
import { News } from "./entities/news.entity";
@Injectable()
export class NewsRepository {
    private readonly table = "news";
    private readonly client:DynamoDBClient;

    constructor(){
        this.client = new DynamoDBClient({
            region: "eu-north-1"
        })
    }

    async findAll(){
        const result:News[] = []
        const command = new ScanCommand({
            TableName:this.table
        })
        const response = await this.client.send(command)

        if(response.Items){
            response.Items.forEach(item => {
                result.push(News.newInstanceFromDynamoDBObject(item))
            })
        }


        return result
    }

    async findNewsBySource(source: string) {
        const result:News[] = []
        const command = new ScanCommand({
            TableName:this.table,
            FilterExpression: '#src = :val', // Filter expression to match the value in the "source" attribute
            ExpressionAttributeNames: {
                '#src': 'source' // Attribute name substitution
            },
            ExpressionAttributeValues: {
                ':val': { S: source } // Value to match in the "source" attribute
            }
        })
        const response = await this.client.send(command)

        if(response.Items){
            response.Items.forEach(item => {
                result.push(News.newInstanceFromDynamoDBObject(item))
            })
        }

        return result
    }
}