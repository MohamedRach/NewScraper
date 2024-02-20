export class News {
    id: string;
    created_at: Date;
    img?: string;
    link: string;
    source: string;
    

    static newInstanceFromDynamoDBObject(data: any): News {
        const result = new News()
        result.id = data.id.S;
        result.img = data?.img?.S;
        result.link = data.link.S;
        result.source = data.source.S;
        result.created_at = new Date(data.created_at.S)
        return result
    }

}
