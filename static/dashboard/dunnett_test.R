#install.packages("DescTools")
library(DescTools)

get_dunnett_test_result = function(df_data){
    set.seed(1)
    result = DunnettTest(df_data)$'1'
    return(list(result, colnames(result), rownames(result)))
}