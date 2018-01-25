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

  *getDumpFile() << "<file> " << splitted_path[splitted_path.size() - 1] << " </file>" << std::endl;

  *getDumpFile() <<"<class><className>" << D->getName().str() << "</className>"<< std::endl;

  clang::RecursiveASTVisitor<Visitor>::TraverseCXXRecordDecl(D);
  *getDumpFile() << "</class>" << std::endl;
  return true;
}

/**********************/
/* If traverse        */
/**********************/

bool Visitor::TraverseIfStmt(clang::IfStmt *S) {
  *getDumpFile()<<"<if>" << std::endl;
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

}

/***********************/
/* C++ Method traverse */
/***********************/
bool Visitor::TraverseCXXMethodDecl(clang::CXXMethodDecl *D) {

  if (!D->isThisDeclarationADefinition()) {
    return true;
  }

  *getDumpFile() << "<method> <methodName> " << D->getName().str() << " </methodName>" << std::endl;

  clang::RecursiveASTVisitor<Visitor>::TraverseCXXMethodDecl(D);

  *getDumpFile() << "</method>" << std::endl;

  return true;
}

bool Visitor::TraverseFunctionDecl(clang::FunctionDecl *D) {

  *getDumpFile() << "<function> <functionName> " << D->getName().str() << "</functionName>" << std::endl;

  clang::RecursiveASTVisitor<Visitor>::TraverseFunctionDecl(D);

  *getDumpFile() << "</function>" << std::endl;

}

/*
 * Var declare
 * */

bool Visitor::VisitVarDecl(clang::VarDecl *D) {

  *getDumpFile() << "<var></var>" << std::endl;

  return true;
}

/*
 * Break statement visit
 * */

bool Visitor::VisitBreakStmt(clang::BreakStmt *D) {

  *getDumpFile() << "<break></break>" << std::endl;
  return true;

}
