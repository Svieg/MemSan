#include "Visitor.h"

/**********************/
/* C++ Class traverse */
/**********************/
bool Visitor::TraverseCXXRecordDecl(clang::CXXRecordDecl *D) {

  std::string file_path = context_.getSourceManager().getFilename(D->getLocation()).str();

  std::stringstream ss(file_path);
  std::string token;
  std::vector<std::string> splitted_path;

  while (std::getline(ss, token, '/')) {
    splitted_path.push_back(token);
  }

  *getDumpFile() << "<filename> " << splitted_path[splitted_path.size() - 1] << " </filename>" << std::endl;

  *getDumpFile() <<"<class><className>" << D->getName().str() << "</className>"<< std::endl;

    if (D->getNumBases() == 1) {

        clang::CXXRecordDecl::base_class_iterator it = D->bases_begin();
        *getDumpFile() <<"<parentClass>" << it->getType().getAsString() << "</parentClass>"<< std::endl;

    }

  clang::RecursiveASTVisitor<Visitor>::TraverseCXXRecordDecl(D);
  *getDumpFile() << "</class>" << std::endl;
  return true;
}

/**********************/
/* If traverse        */
/**********************/

bool Visitor::TraverseIfStmt(clang::IfStmt *S) {
  unsigned int line = context_.getSourceManager().getPresumedLoc(S->getLocStart(), 1).getLine();
  *getDumpFile()<<"<if>" << line << std::endl;
  clang::RecursiveASTVisitor<Visitor>::TraverseIfStmt(S);
  *getDumpFile()<<"</if>" << std::endl;

  return true;
}

/*
 * While Stmt traverse
 * */

bool Visitor::TraverseWhileStmt(clang::WhileStmt *S) {

  *getDumpFile() << "<while>" << std::endl;
  clang::RecursiveASTVisitor<Visitor>::TraverseWhileStmt(S);
  *getDumpFile() << "</while>" << std::endl;
    return true;

}

/***********************/
/* C++ Method traverse */
/***********************/
bool Visitor::TraverseCXXMethodDecl(clang::CXXMethodDecl *D) {

    if (!D->isThisDeclarationADefinition()) {
        return true;
    }

    *getDumpFile() << "<method>" << std::endl;
    *getDumpFile() << "<methodName>" << D->getName().str() << "</methodName>" << std::endl;
    /*if (D->isPublic()) {
        *getDumpFile() << "<methodScope>public</methodScope>" << std::endl;
    }
    else {
        *getDumpFile() << "<methodScope>private</methodScope>" << std::endl;
    }*/
    *getDumpFile() << "<methodReturnType>" << D->getResultType().getAsString() << "</methodReturnType>" << std::endl;

    clang::RecursiveASTVisitor<Visitor>::TraverseCXXMethodDecl(D);

    *getDumpFile() << "</method>" << std::endl;

    return true;
}

bool Visitor::TraverseFunctionDecl(clang::FunctionDecl *D) {

  *getDumpFile() << "<function> <functionName> " << D->getName().str() << "</functionName>" << std::endl;

  clang::RecursiveASTVisitor<Visitor>::TraverseFunctionDecl(D);

  *getDumpFile() << "</function>" << std::endl;
    return true;

}

/*
 * Var declare
 * */

bool Visitor::VisitVarDecl(clang::VarDecl *D) {

  *getDumpFile() << "<var> " << D->getName().str() << " </var>" << std::endl;

  return true;
}

/*
 * Break statement visit
 * */

bool Visitor::VisitBreakStmt(clang::BreakStmt *D) {

  *getDumpFile() << "<break></break>" << std::endl;
  return true;

}

/*
 * Attributes visit
 * */

bool Visitor::VisitFieldDecl(clang::FieldDecl *D) {

    *getDumpFile() << "<attribute>" << std::endl;
    *getDumpFile() << "<attributeName>" << D->getName().str() << "</attributeName>" << std::endl;
    *getDumpFile() << "<attributeType>" << D->getType().getAsString() << "</attributeType>" << std::endl;
    /*if (D->isPublic()) {
        *getDumpFile() << "<attributeScope>public</attributeScope>" << std::endl;
    }
    else {
        *getDumpFile() << "<methodScope>private</methodScope>" << std::endl;
    }*/

    *getDumpFile() << "</attribute>" << std::endl;
    return true;

}

/*
 * Return statement traverse
 * */

bool Visitor::TraverseReturnStmt(clang::ReturnStmt *D) {

    *getDumpFile() << "<return>" << std::endl;
    clang::RecursiveASTVisitor<Visitor>::TraverseReturnStmt(D);
    *getDumpFile() << "</return>" << std::endl;
  return true;
}

bool Visitor::VisitContinueStmt(clang::ContinueStmt *D) {

    *getDumpFile() << "<continue></continue>" << std::endl;
  return true;

}


bool Visitor::TraverseForStmt(clang::ForStmt *D) {

    *getDumpFile() << "<for>" << std::endl;
    clang::RecursiveASTVisitor<Visitor>::TraverseForStmt(D);
    *getDumpFile() << "</for>" << std::endl;
  return true;

}

bool Visitor::VisitUnaryOperator(clang::UnaryOperator *D) {

    *getDumpFile() << "<unaryOperator></unaryOperator>" << std::endl;
  return true;

}

bool Visitor::VisitBinaryOperator(clang::BinaryOperator *D) {

    *getDumpFile() << "<binaryOperator></binaryOperator>" << std::endl;
  return true;

}
